import json
import time
import uuid

import requests
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView

from account.forms import SignUpForm, LoginForm, UserEditForm
from account.models import Organisation
from core.utils import get_database_data
from projects.mixins import ProjectsListMixin
from streamprocessors.druid_utils import get_payload_interval
from streamprocessors.kafka_utils import send_kafka_message
from streamprocessors.models import WorkflowTask


class UserCreateView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'account/signup/signup.html'
    success_url = reverse_lazy('projects:projects_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        to_return = super().form_valid(form)
        obj = form.save(commit=False)
        company_id = self.request.session.get("company_id")
        if company_id:
            organisation = Organisation.objects.get(pk=company_id)
            obj.organisation_owner = False
            organisation = Organisation.objects.get(company_name=organisation.company_name)
        else:
            cleaned_data = form.cleaned_data
            organisation = Organisation.objects.create(
                company_name=cleaned_data.get("organisation__company_name"),
                default_druid_url=settings.DRUID_URL,
                default_kafka_url=settings.KAFKA_URL,
                kafka_url_public=settings.KAFKA_URL_PUBLIC,
                default_cluster_endpoint=settings.DOCKER_BASE_URL
            )
            print( f"KAFKA_URL_PUBLIC is {settings.KAFKA_URL_PUBLIC}" )

        obj.organisation = organisation
        obj.save()
        if company_id:
            del self.request.session["company_id"]
        user = authenticate(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return


class UserLoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('projects:projects_list')
    template_name = 'account/registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form, **kwargs):
        form.errors['wrong_credentials'] = True
        return super().form_invalid(form)


class UserEditView(LoginRequiredMixin, generic.UpdateView, ProjectsListMixin):
    form_class = UserEditForm
    model = get_user_model()
    template_name = 'account/edit/edit.html'
    success_url = reverse_lazy('projects:projects_list')

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context


class WorkflowTasksView(LoginRequiredMixin, ListView, ProjectsListMixin):
    template_name = 'account/workflow/index.html'
    model = WorkflowTask
    context_object_name = 'workflows'
    druid_host, druid_port = get_database_data()

    def get_queryset(self):
        return self.model.objects.filter(recipient=self.request.user).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        reassign_user = request.GET.get('reassign')

        paginator = Paginator(context['data'], 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        if reassign_user:
            self.reassign_task(reassign_user)
            return HttpResponseRedirect(reverse_lazy('account:workflow-tasks', kwargs={'user_id': request.user.id}))
        return self.render_to_response(context)

    def reassign_task(self, reassign_user):
        workflow_id = self.request.GET.get('task')
        workflow_topic = 'Realtime-Data-analysist-platform'
        user_id = self.request.user.id

        exists_task = self.get_exists_task(workflow_topic, workflow_id, reassign_user)
        if not exists_task:
            new_task = self.get_exists_task(workflow_topic, workflow_id, user_id)
            if new_task:
                new_task['recipient'] = reassign_user
                new_task['timestamp'] = new_task.pop('_0', int(time.time() * 1000))
                new_task['uuid'] = str(uuid.uuid4())
                new_task = json.dumps(new_task)
                send_kafka_message(topic=workflow_topic, message=new_task)

        workflow_task = self.model.objects.get(id=workflow_id)
        if workflow_task.recipient_id != int(reassign_user):
            workflow_task.recipient_id = reassign_user
            workflow_task.save()

    def get_exists_task(self, workflow_topic: str, workflow_id: int, user_id: int):
        # query = f'SELECT DISTINCT * FROM "{workflow_topic}"
        # WHERE workflow_id={workflow_id} AND recipient={user_id}'
        payload = {
            "queryType": "groupBy",
            "dataSource": {
                "type": "table",
                "name": workflow_topic
            },
            "intervals": {
                "type": "intervals",
                "intervals": [get_payload_interval(default=True)]
            },
            "filter": {
                "type": "and",
                "fields": [
                    {
                        "type": "selector",
                        "dimension": "workflow_id",
                        "value": f"{workflow_id}",
                    },
                    {
                        "type": "selector",
                        "dimension": "recipient",
                        "value": f"{user_id}",
                    }
                ]
            },
            "granularity": {
                "type": "all"
            },
            "dimensions": [
                {
                    "type": "default",
                    "dimension": "__time",
                    "outputName": "_0",
                    "outputType": "LONG"
                },
                {
                    "type": "default",
                    "dimension": "event",
                    "outputName": "event",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "project_id",
                    "outputName": "project_id",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "recipient",
                    "outputName": "recipient",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "task_description",
                    "outputName": "task_description",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "task_title",
                    "outputName": "task_title",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "uuid",
                    "outputName": "uuid",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "workflow_id",
                    "outputName": "workflow_id",
                    "outputType": "STRING"
                }
            ],
            "limitSpec": {
                "type": "NoopLimitSpec"
            },
            "descending": False
        }

        response = requests.post(f'http://{self.druid_host}:{self.druid_port}/druid/v2/?pretty',
                                 headers={'Content-Type': 'application/json'}, json=payload)
        if response.status_code == 200:
            try:
                data = response.json()
                return data[0].get('event')
            except:
                return {}
        else:
            return {}

    def get_context_data(self, *args, **kwargs):
        context = super(WorkflowTasksView, self).get_context_data(*args, **kwargs)
        self.set_projects(context)

        workflow_tasks_ids = [f"{i}" for i in tuple(self.get_queryset().values_list('id', flat=True))]

        # query = f'SELECT DISTINCT workflow_id, task_title, task_description ' \
        #         f'FROM "Realtime-Data-analysist-platform" WHERE workflow_id in {workflow_tasks}'
        """ Druid does not yet have full support for joins!!! to use DISTINCT and at the same time order by time! """
        payload = {
            "queryType": "groupBy",
            "dataSource": {
                "type": "table",
                "name": "Realtime-Data-analysist-platform"
            },
            "intervals": {
                "type": "intervals",
                "intervals": [get_payload_interval(default=True)]
            },
            "filter": {
                "type": "in",
                "dimension": "workflow_id",
                "values": workflow_tasks_ids,
            },
            "granularity": {
                "type": "all"
            },
            "dimensions": [
                {
                    "type": "default",
                    "dimension": "__time",
                    "outputName": "time",
                    "outputType": "LONG"
                },
                {
                    "type": "default",
                    "dimension": "workflow_id",
                    "outputName": "workflow_id",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "task_title",
                    "outputName": "task_title",
                    "outputType": "STRING"
                },
                {
                    "type": "default",
                    "dimension": "task_description",
                    "outputName": "task_description",
                    "outputType": "STRING"
                }
            ],
            "limitSpec": {
                "type": "default",
                "columns": [
                    {
                        "dimension": "time",
                        "direction": "descending",
                        "dimensionOrder": {
                            "type": "numeric"
                        }
                    }
                ],
                "limit": 2147483647
            },
            "descending": False
        }
        response = requests.post(f'http://{self.druid_host}:{self.druid_port}/druid/v2/?pretty',
                                 headers={'Content-Type': 'application/json'}, json=payload)
        if response.status_code == 200:
            try:
                data = response.json()
                data_list = list(map(lambda i: i.get('event'), data))
                for item in data_list:
                    item['workflow_id'] = int(item.get('workflow_id', 0))
            except:
                data_list = []
        else:
            data_list = []

        context['data'] = data_list

        users = get_user_model().objects.values('id', 'first_name', 'last_name', 'email')
        context['users'] = users

        return context


class WorkflowDeleteView(LoginRequiredMixin, generic.DeleteView, ProjectsListMixin):
    template_name = 'account/workflow/delete.html'
    model = WorkflowTask
    pk_url_kwarg = 'workflow_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.recipient != request.user:
            return HttpResponseRedirect(self.get_success_url())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('account:workflow-tasks', kwargs={'user_id': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super(WorkflowDeleteView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.recipient = None
        self.object.save()
        return HttpResponseRedirect(success_url)


class UserHelpView(TemplateView, ProjectsListMixin):
    template_name = 'account/generals/help.html'

    def get_context_data(self, **kwargs):
        context = super(UserHelpView, self).get_context_data(**kwargs)
        self.set_projects(context)
        return context


class OrganisationView(generic.RedirectView):

    url = reverse_lazy('account:signup')

    def get(self, request, *args, **kwargs):
        invite_key = kwargs.get("invite_key")
        try:
            organisation = Organisation.objects.get(invite_key=invite_key)
        except Exception as error:
            return super().get(request, *args, **kwargs)
        request.session["company_id"] = organisation.id
        return super().get(request, *args, **kwargs)

@csrf_exempt
def validate_developer_key(request):
    developer_key = request.POST.get('key')
    user = get_user_model().objects.filter(developer_key=developer_key)
    response, status = {'status': 'confirmed'}, 200
    if not user.exists():
        response['status'], status = 'denied', 403
    return HttpResponse(json.dumps(response), content_type='application/json', status=status)
