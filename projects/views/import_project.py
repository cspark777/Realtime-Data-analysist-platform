import json
import random
from http import HTTPStatus
from mptt.models import TreeForeignKey

from django.apps import apps, config
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.fields.related import ForeignKey
from django.http import HttpResponse

from projects.models import Project


@login_required
@transaction.atomic
def import_project(request):
    try:
        prj_name = request.FILES.get('file').name.split('.')[0]
        prj_description = 'prj_description'
    except:
        prj_name = 'Project_%s' % random.randint(1, 100)
        prj_description = 'Description_%s' % random.randint(1, 100)

    prj = Project(name=prj_name, description=prj_description, created_by=request.user)
    prj.save()
    project_id = prj.pk

    models, models_dict = inner_models_resolution()
    table_fields_to_replace = get_table_fields_to_replace(models)

    file = request.FILES.get('file').read()
    records = json.loads(file)

    primary_keys = list(map(lambda rec: {rec.get('model', '.').split('.')[1]: {'old': rec.get('pk')}}, records))

    for record in records:
        sql_model = record.get('model', '.')
        _, field_to_check = sql_model.split('.')

        model = models_dict.get(sql_model)

        sql_fields = record.get('fields')
        kwargs = get_sql_objects(table_fields_to_replace, sql_fields)
        kwargs = {key: value if key != 'project_id' else project_id for key, value in kwargs.items()}

        new_kwargs = dict()

        old_pk_object = record.get('pk')
        primary_key = list(filter(lambda primary_key: primary_key.get(field_to_check, {}).get('old') == old_pk_object,
                                  filter(lambda i: i.get(field_to_check), primary_keys)))
        primary_key = primary_key[0] if primary_key else {}

        for key, value in kwargs.items():
            if key in table_fields_to_replace.values() and key != 'project_id':
                if key in ('created_by_id', 'owning_user_id'):
                    value = request.user.id if value else None
                else:
                    key_for_check = key[:-3] if key != 'parent_id' else 'streamprocessorstep'
                    value = list(filter(lambda primary_key: primary_key.get(key_for_check, {}).get('old') == value,
                                        filter(lambda i: i.get(key_for_check), primary_keys)))
                    value = value[0] if value else {}
                    value = value.get(key_for_check, {}).get('new')
            new_kwargs[key] = value

        item = model.objects.create(**new_kwargs)
        primary_key[field_to_check]['new'] = item.pk
    return HttpResponse(HTTPStatus.OK)


def inner_models_resolution():
    disallow_apps = ['account', 'core']
    applications = {name: app for name, app in apps.app_configs.items()
                    if type(app) is config.AppConfig and name not in disallow_apps}

    models_list = list(
        map(lambda app: list(map(lambda i: (f'{app[0]}.{i[0]}', i[1]._meta.model), app[1].models.items())),
            applications.items()))
    models_list = dict([item for sublist in models_list for item in sublist])

    models = filter(None, map(lambda app: app.models, applications.values()))
    models = map(lambda model: model.values(), models)
    return models, models_list


def get_table_fields_to_replace(models):
    fields_to_replace = dict()
    for app_models in models:
        for model in app_models:
            foreign_keys = filter(lambda m: type(m) in (ForeignKey, TreeForeignKey), model._meta.fields)
            fields = dict(map(lambda related: (getattr(related, 'name'), getattr(related, 'attname')), foreign_keys))
            fields_to_replace.update(fields)

    return fields_to_replace


def get_sql_objects(objects_to_replace, non_sql_object):
    data = dict()
    for field, value in non_sql_object.items():
        data[objects_to_replace.get(field, field)] = value
    return data
