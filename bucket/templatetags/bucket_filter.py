from django import template

register = template.Library()

@register.filter
def is_bucket(value):
    if value.count('/') == 1:
        return True
    return False

@register.filter
def upper_path(value):
    folders = value.split('/')
    path = ''
    for i in range(len(folders)-2):
        path += folders[i] + '/'
    return path