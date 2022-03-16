def save_object(obj, **kwargs):
    for key, value in kwargs.items():
        setattr(obj, key, value)
    obj.save()


def filter_contains(initial_dict, filter_by, is_contains=True):
    if is_contains:
        return {name: value for name, value in initial_dict.items() if name.__contains__(filter_by)}
    return {name: value for name, value in initial_dict.items() if not name.__contains__(filter_by)}


def filter_endswith(initial_dict, filter_by):
    return {name.replace(filter_by, ''): value for name, value in initial_dict.items() if name.endswith(filter_by)}
