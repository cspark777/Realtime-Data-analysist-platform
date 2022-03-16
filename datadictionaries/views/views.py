from re import search

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from datadictionaries.models import DataDictionary, DataItem
from .utils import save_object, filter_endswith, filter_contains


@login_required
def duplicate_datadictionary(request, project_id, datadictionary_id):
    datadictionary = DataDictionary.objects.get(pk=datadictionary_id)
    if datadictionary.project_id == project_id:
        method_duplicate_datadictionary(project_id, datadictionary)

    return HttpResponseRedirect(reverse_lazy('projects:datadictionaries:datadictionaries_list', kwargs={'project_id': project_id}))


def method_duplicate_datadictionary(project_id, datadictionary):
    items = datadictionary.items.all()
    datadictionary.pk = None
    datadictionary.project_id = project_id
    datadictionary.save()

    for item in items:
        item.pk = None
        item.datadictionary = datadictionary
        item.save()


def save_datadictionary(view, form, data, datadictionary, cleaned_data):
    try:
        save_object(obj=datadictionary, **cleaned_data)
    except Exception as error:
        return view.form_invalid(form, exception=error)

    # Process source: mapped values (items)
    items = datadictionary.items.all()
    initial_count_items = items.count()
    ordering_data = filter_contains(initial_dict=data, filter_by='ordering')
    delete_items = filter_contains(initial_dict=ordering_data, filter_by='delete')
    delete_items = list(map(lambda key: int(key.rsplit('_', 1)[1]), delete_items.keys()))
    ordering_data = filter_contains(initial_dict=ordering_data, filter_by='delete', is_contains=False)
    items_data = filter_contains(initial_dict=data, filter_by='_')
    new_items = {key: view.request.POST[key] for key in view.request.POST if
                 '_new_' in key and not key.startswith('delete_')}
    old_items = {name: value for name, value in items_data.items() if name not in new_items}
    new_count_items = len(set(ordering_data.values()))
    new_items_list = [search(r'\d+$', key).group(0) for key in new_items if 'source_value_' in key]

    # Check for duplicates
    if new_count_items < initial_count_items and not delete_items:
        error = 'Duplicate source values not allowed'
        return view.form_invalid(form, exception=error)

    # Process existing items
    for item in items:
        if item.id in delete_items:
            item.delete()
            continue
        item_info = filter_endswith(initial_dict=old_items, filter_by='_%s' % item.id)
        try:
            save_object(obj=item, **item_info)
        except Exception as error:
            return view.form_invalid(form, exception=error)
    # Add new items
    for new_id in new_items_list:
        item_info = filter_endswith(initial_dict=new_items, filter_by='_new_%s' % new_id)
        item_info['datadictionary'] = datadictionary
        item = DataItem()

        try:
            save_object(obj=item, **item_info)
        except Exception as error:
            return view.form_invalid(form, exception=error)

    return HttpResponseRedirect(view.get_success_url())
