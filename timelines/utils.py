import re


def template_replace(template, each):
    list_of_keys = re.findall(r'{.*?}', template)
    for key in list_of_keys:
        template = template.replace(key, f'{getattr(each, key[1:-1], "<Not Found>")}')
    return template
