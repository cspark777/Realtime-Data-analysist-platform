import json
from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from pydruid.db import connect

from analysis.models import Report, ReportItem
from core.utils import get_database_data, generate_avro
from datadictionaries.models import DataDictionary
from projects.mixins import set_projects
from projects.models import Project
from simulations.models import Simulation
from streamprocessors.druid_utils import get_payload_interval, execute_druid_query, correct_schema_names
from streamprocessors.forms import TestSimulateForm
from streamprocessors.kafka_utils import send_kafka_message
from streamprocessors.models import StreamProcessor, StreamProcessorStep, WorkflowTask
from streams.models import Stream
from streams.utils import parse_simple_time_interval

kafka_url = settings.KAFKA_URL
druid_host, druid_port = get_database_data()


def rows_to_json(curs):
    json_objects = []
    for row in curs:
        record = {}
        for field in row._fields:
            record[field] = getattr(row, field)
        json_objects.append(record)
    return json_objects


def public_streamprocessor_run(request, project_id, streamprocessor_id):
    streamprocessor = StreamProcessor.objects.filter(pk=streamprocessor_id, project_id=project_id)
    if not streamprocessor.exists():
        return HttpResponseRedirect(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                                                 kwargs={'project_id': project_id}))

    streamprocessor = streamprocessor.first()
    queryset = streamprocessor.streamprocessorstep_set.all().order_by('ordering')
    dsl = {
        'DAGStreamProcessorName': streamprocessor.name,
        'DAGLayout': {},
        'DAGNodes': [],
        'DAGDataMappings': []
    }

    for index, step in enumerate(queryset, start=1):
        dsl['DAGLayout']["DAGNode%s" % str(index)] = [
            "DAGNode%s" % str(index + 1)] if index < queryset.count() else []
        step_types_data = step.STEP_TYPES_DATA
        step_types_data.update(WorkflowTask.STEP_TYPES_DATA)
        data = {"Name": step.name, "Description": step.description,
                "Type": step_types_data[step.steptype]['step_type_name']}
        for field in step.STEP_TYPES_DATA[step.steptype]['fields']:
            if field['name'] == 'block':
                children = step.get_children()
                if any(children):
                    data.update({'Block': get_child_block_data(children, field['fields'])})
                else:
                    data.update({'Block': ''})
            else:
                field_name = ''.join(map(lambda item: item.capitalize(), field['name'].split('_')))
                additional_data = {}
                if step.steptype == StreamProcessorStep.WORKFLOW:
                    workflow = step.workflowtask_set.filter().first()
                    inner_data = {field_name: getattr(workflow, field['name'].replace('task_', ''), '')}
                    additional_data['WorkflowId'] = workflow.id
                elif step.steptype == StreamProcessorStep.FUNCTION:
                    inner_data = {field_name: getattr(step, field['name'], '')}
                    additional_data['FunctionId'] = 0
                else:
                    inner_data = {field_name: getattr(step, field['name'], '')}
                inner_data.update(additional_data)
                data.update(inner_data)

        avro = None
        inbound_topic = None
        operator = None
        if step.steptype in ('inbound', 'outbound', 'transcribe'):
            inbound_topic = step.topic
        if step.steptype in ('lookup',):
            inbound_topic = step.record_type
            operator = data.get('Operator')

        if inbound_topic:
            avro = generate_avro(inbound_topic, operator)
        data['AVRO'] = avro

        dsl['DAGNodes'].append(data)

    data_dictionaries = DataDictionary.objects.filter(project=streamprocessor.project)
    dsl['DAGDataMappings'] = [ddict.to_dict() for ddict in data_dictionaries if ddict.items.all()]

    streamprocessor.dsl = json.dumps(dsl)
    streamprocessor.save()

    server_url = settings.DATA_SERVER + 'runstreamprocessor'
    data = streamprocessor.dsl
    data = json.dumps(
        {
            'message': data,
            'user': request.user.id,
            'project_id': project_id,
            'streamprocessor_id': streamprocessor_id,
            'broker_url': kafka_url,
            'database_url': settings.DRUID_URL,
            'replicas': streamprocessor.replicas,
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'sender_email': settings.SENDER_EMAIL,
            'additional_uuid_integrity_check': streamprocessor.additional_integrity_checks,
            'delay_on_uuid_failure': streamprocessor.delay_on_uuid_failure,
            'retry_on_uuid_failure_count': streamprocessor.retry_on_uuid_failure_count,
            'DATA_function_url': settings.DATA_FUNCTION_URL,
        }
    )

    print(f"Request to deploy StreamProcessor [{streamprocessor.name}].  Post Data Follows.")
    print('data:', data)

    return requests.post(server_url, data=data).status_code


@login_required
def streamprocessor_run(request, project_id, streamprocessor_id):
    status = public_streamprocessor_run(request, project_id, streamprocessor_id)

    print("Executed!")
    url = reverse_lazy('projects:streamprocessors:streamprocessors_after_run',
                       kwargs={'project_id': project_id,
                               'streamprocessor_id': streamprocessor_id,
                               'status': status})
    return redirect(url)


def get_child_block_data(children: list, fields: list) -> list:
    blocks_data = []
    for child in children:
        child_data = {}
        for block_field in fields:
            field_name = ''.join(map(lambda item: item.capitalize(), block_field['name'].split('_')))
            inner_data = {field_name: getattr(child, block_field['name'], '')}
            child_data.update(inner_data)
        blocks_data.append(child_data)
    return blocks_data


def public_streamprocessor_stop(request, project_id, streamprocessor_id):
    streamprocessor = StreamProcessor.objects.filter(pk=streamprocessor_id, project_id=project_id)
    if not streamprocessor.exists():
        return HttpResponseRedirect(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                                                 kwargs={'project_id': project_id}))
    streamprocessor = streamprocessor.first()
    streamprocessor.is_running = False
    streamprocessor.save()
    server_url = settings.DATA_SERVER + 'stopstreamprocessor'
    data = json.dumps(
        {
            'project_id': project_id,
            'streamprocessor_id': streamprocessor_id,
            'user': request.user.id,
        }
    )
    return requests.post(server_url, data=data).status_code


@login_required
def streamprocessor_stop(request, project_id, streamprocessor_id):
    status = public_streamprocessor_stop(request, project_id, streamprocessor_id)

    print(f"Status on stopping container [{status}]")
    url = reverse_lazy('projects:streamprocessors:streamprocessors_after_run',
                       kwargs={'project_id': project_id,
                               'streamprocessor_id': streamprocessor_id,
                               'status': status})
    return redirect(url)


@login_required
def duplicate_streamprocessor(request, project_id, streamprocessor_id):
    streamprocessor = StreamProcessor.objects.get(pk=streamprocessor_id)
    if streamprocessor.project_id == project_id:
        method_duplicate_streamprocessor(project_id, streamprocessor)

    return redirect(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                                 kwargs={'project_id': project_id}))


def method_duplicate_streamprocessor(project_id, streamprocessor):
    steps = StreamProcessorStep.objects.filter(streamprocessor=streamprocessor)

    streamprocessor.pk = None
    streamprocessor.project_id = project_id
    streamprocessor.save()

    for step in steps:
        block_steps = step.get_children()
        kwargs = model_to_dict(step, exclude=['id', 'tree_id'])
        kwargs['streamprocessor'] = streamprocessor
        new_step = StreamProcessorStep.objects.create(**kwargs)
        for block_step in block_steps:
            new_kwargs = model_to_dict(block_step, exclude=['id', 'tree_id'])
            new_kwargs['parent'] = new_step
            StreamProcessorStep.objects.create(**new_kwargs)


@login_required
def streamprocessor_test(request, project_id):
    form = TestSimulateForm(request.POST or None)
    print(form)
    print(form.is_valid())
    if form.is_valid():
        event = form.cleaned_data['event']
        stream = form.cleaned_data['stream']
        send_kafka_message(stream, event)

    stream_list = Stream.objects.filter(project=project_id)
    context = {'stream_list': stream_list, 'form': form}
    set_projects(context, request=request)
    return render(request, 'streamprocessors/testsimulate.html', context)


@login_required
def stream_analyse(request, project_id, stream_id):
    stream = Stream.objects.get(pk=stream_id)
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()
    query = "SELECT DISTINCT * FROM " + stream.name
    print("About to execute query " + query)
    curs.execute(query)
    row = curs.fetchone()
    keys = row._fields
    context = {'rows': rows_to_json(curs), 'keys': keys}
    set_projects(context, request=request)
    return render(request, 'streams/analyse_streams.html', context)


@login_required
def source_events(request, project_id, object_id):
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()

    stream_name = None
    limit = request.GET.get('limit', '5000')
    search_stream = request.GET.get('search_stream')
    is_file = request.GET.get('is_file')
    if search_stream:
        stream_name = search_stream
        stream = Stream.objects.get(project_id=project_id, name=stream_name)
        limit = '5000'
    is_not_logs = all(map(lambda i: i.isdigit(), object_id))
    if is_not_logs and not stream_name:
        if limit:
            try:
                report_item = Report.objects.get(pk=object_id).reportitem_set.filter(type=ReportItem.DATA_TABLE).first()
                if report_item:
                    stream = Stream.objects.get(name=report_item.record_type)
                else:
                    stream = Stream.objects.get(pk=object_id)
            except Report.DoesNotExist:
                stream = Stream.objects.get(pk=object_id)
        else:
            stream = Stream.objects.get(pk=object_id)
        stream_name = stream.name
    elif not stream_name:
        stream_name = 'DATA_logs'

    query = "SELECT DISTINCT * FROM " + f'"{stream_name}"'
    where = ' WHERE '
    filter_ = request.GET.get('filter')
    if filter_:
        query += where + filter_
    if not is_not_logs:
        query += f'{where if where not in query else " AND "}project_id = {project_id}'
        if hasattr(get_user_model(), 'role') and request.user.role == get_user_model().USER:
            query += ' AND message_type != code_exception'

    interval = request.GET.get('interval_field', '')
    time_window = ''
    if interval:
        interval_value, interval_type = parse_simple_time_interval(interval)
        if interval_value != 'error':
            time_window = f" __time > TIMESTAMPADD({interval_type}, -{interval_value}, CURRENT_TIMESTAMP)"
    if time_window:
        query += f'{where if where not in query else " AND "}{time_window}'

    query += ' ORDER BY __time DESC '
    if limit and int(limit):
        query += ' LIMIT ' + limit

    try:
        print(f"Executing the Druid Query [{query}]")
        source_data_keys_events, source_data_rows = correct_schema_names(execute_druid_query(query, curs),
                                                                         stream.schema)
    except:
        return render_not_found(request, stream_name)
    for obj in source_data_rows:
        if '__time' in obj.keys():
            obj['__time'] = datetime.strptime(obj['__time'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime(
                '%m-%d-%Y %H:%M:%S.%f')[:-3]
        if 'streamprocessor_id' in obj.keys() and obj['streamprocessor_id'].isdigit():
            streamprocessor = StreamProcessor.objects.filter(id=obj['streamprocessor_id']).first()
            if streamprocessor:
                obj['streamprocessor_id'] = streamprocessor.name
    if source_data_rows:
        if source_data_rows[0].get('count'):
            source_data_rows = sorted(source_data_rows, key=lambda k: k['count'], reverse=True)

    response = HttpResponse(json.dumps({'data': source_data_rows}), content_type='application/json')
    if is_file:
        response['Content-Disposition'] = 'attachment; filename="events.json"'
    return response


@login_required
def source_events_summary(request, project_id, object_id):
    try:
        fields = request.GET.get('fields').split(',')
    except ValueError:
        return HttpResponse()
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()

    is_not_logs = all(map(lambda i: i.isdigit(), object_id))
    if is_not_logs:
        stream = Stream.objects.get(pk=object_id)
        stream_name = stream.name
    else:
        stream_name = 'DATA_logs'

    counts = [f'COUNT({field.strip()}) AS {field.strip()}' for field in fields]

    query = f"SELECT {', '.join(counts)} FROM " + stream_name
    where = ' WHERE '
    filter_ = request.GET.get('filter')
    if filter_:
        query += where + filter_
    if not is_not_logs:
        query += f'{where if where not in query else " AND "}project_id = {project_id}'
        if hasattr(get_user_model(), 'role') and request.user.role == get_user_model().USER:
            query += ' AND message_type != code_exception'

    try:
        print(f"Executing the Druid Query [{query}]")
        source_data_keys_events, source_data_rows = execute_druid_query(query, curs)
    except:
        return render_not_found(request, stream_name)

    if source_data_rows:
        if source_data_rows[0].get('count'):
            source_data_rows = sorted(source_data_rows, key=lambda k: k['count'], reverse=True)

    print(f"Returned Rows Are [{source_data_rows}]")

    return HttpResponse(json.dumps({'data': source_data_rows}), content_type='application/json')


@login_required
def get_logs_rows(request, project_id):
    payload = {
        'queryType': 'scan',
        'dataSource': 'DATA_logs',
        'granularity': 'all',
        'intervals': [get_payload_interval(default=True)],
        'filter': {
            "type": "and",
            'fields': [
                {
                    "type": "in",
                    "dimension": "project_id",
                    "values": list(Project.objects.filter(created_by=request.user).values_list('id', flat=True)),
                    # "values": [project_id],
                }
            ]
        },
        'columns': ['__time', 'component', 'message', 'message_type', 'priority', 'project_id', 'simulation_id',
                    'streamprocessor_id'],
        'limit': '750',
        'order': 'descending'
    }
    if request.GET:
        project = request.GET.get('project')
        processor = request.GET.get('processor')
        priority = request.GET.get('priority')
        component = request.GET.get('component')
        simulation = request.GET.get('simulation')
        time = request.GET.get('time')
        if hasattr(get_user_model(), 'role') and request.user.role == get_user_model().USER:
            payload['filter']['fields'].append({
                'type': 'not',
                'field': [
                    {
                        'type': 'selector',
                        'dimension': 'message_type',
                        'value': 'code_exception'
                    }
                ]
            })
        if project and project != 'all':
            payload['filter']['fields'].append({
                'type': 'selector',
                'dimension': 'project_id',
                'value': project
            })
        if processor and processor != 'all':
            payload['filter']['fields'].append({
                'type': 'selector',
                'dimension': 'streamprocessor_id',
                'value': processor
            })
        if simulation and simulation != 'all':
            payload['filter']['fields'].append({
                'type': 'selector',
                'dimension': 'simulation_id',
                'value': simulation
            })
        if priority and priority != 'all':
            payload['filter']['fields'].append({
                'type': 'selector',
                'dimension': 'priority',
                'value': priority
            })
        if component and component != 'all':
            payload['filter']['fields'].append({
                'type': 'selector',
                'dimension': 'component',
                'value': component
            })
        if time:
            payload['intervals'] = [get_payload_interval(time)]
    response = requests.post(f'http://{druid_host}:{druid_port}/druid/v2/?pretty',
                             headers={'Content-Type': 'application/json'}, json=payload)
    rows = []
    if response.status_code == 200:
        data = response.json()
        for i in range(len(data)):
            for item in data[i]['events']:
                temp = datetime.fromtimestamp(int(str(item['__time'])[:10]))
                item['__time'] = temp.strftime(f'%m-%d-%Y %H:%M')
                item['process'] = None
                if item['project_id']:
                    item['project_id'] = Project.objects.get(id=item['project_id']).name if Project.objects.filter(
                        id=item['project_id']).exists() else None
                if item['simulation_id']:
                    item['simulation_id'] = Simulation.objects.get(
                        id=item['simulation_id']).name if Simulation.objects.filter(
                        id=item['simulation_id']).exists() else None
                    item['process'] = item['simulation_id']
                if item['streamprocessor_id']:
                    item['streamprocessor_id'] = StreamProcessor.objects.get(
                        id=item['streamprocessor_id']).name if StreamProcessor.objects.filter(
                        id=item['streamprocessor_id']).exists() else None
                    item['process'] = item['streamprocessor_id']
                rows.append(item)
    return HttpResponse(json.dumps({'data': rows}), content_type='application/json')


@login_required
def get_logs_headers(request, project_id):
    projects = list(Project.objects.filter(created_by=request.user).values('id', 'name'))
    processors = list(StreamProcessor.objects.filter(owning_user=request.user).values('id', 'name'))
    simulations = list(Simulation.objects.filter(created_by=request.user).values('id', 'name'))
    return HttpResponse(json.dumps({"projects": projects, "processors": processors, "simulations": simulations}),
                        content_type='application/json')


@login_required
def view_logs(request, project_id, streamprocessor_id):
    streamprocessor = StreamProcessor.objects.filter(pk=streamprocessor_id, project_id=project_id)
    if not streamprocessor.exists():
        return HttpResponseRedirect(reverse_lazy('projects:streamprocessors:streamprocessors_list',
                                                 kwargs={'project_id': project_id}))
    streamprocessor = streamprocessor.first()
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()

    query = "SELECT DISTINCT __time, component, message, message_type, project_id FROM DATA_logs WHERE streamprocessor_id = " + str(
        streamprocessor_id) + " LIMIT 2"
    try:
        source_data_keys_logs, source_data_rows = execute_druid_query(query, curs)
    except:
        return render_not_found(request, 'DATA_logs')

    context = {
        'source_data_keys_logs': list(source_data_keys_logs),
        'source_data_rows': source_data_rows,
        'streamprocessor': streamprocessor.name,
        'analysis_url': reverse_lazy('projects:streamprocessors:source_logs',
                                     kwargs={'project_id': project_id, 'streamprocessor_id': streamprocessor_id}),
    }
    set_projects(context, request=request)

    return render(request, 'streamprocessors/logs.html', context)


@login_required
def source_logs(request, project_id, streamprocessor_id):
    conn = connect(host=druid_host, port=druid_port, path='/druid/v2/sql/', scheme='http')
    curs = conn.cursor()

    query = "SELECT DISTINCT * FROM DATA_logs WHERE streamprocessor_id = " + str(
        streamprocessor_id) + " AND project_id = " + str(project_id)

    try:
        source_data_keys, source_data_rows = execute_druid_query(query, curs)
    except:
        return render_not_found(request, 'DATA_logs')
    return HttpResponse(json.dumps({'data': source_data_rows}), content_type='application/json')


@login_required
def render_not_found(request, table):
    context = {'table': table}
    set_projects(context, request=request)
    response = render(request, '404.html', context)
    response.status_code = 404
    return response


class Logs(LoginRequiredMixin, TemplateView):
    template_name = 'reports/all_logs.html'

    def get(self, request, *args, **kwargs):
        response = {'': '', }
        set_projects(response, request=request)
        return render(request=request, template_name=self.template_name, context=response)
