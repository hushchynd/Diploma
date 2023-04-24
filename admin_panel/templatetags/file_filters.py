import os

from django import template

register = template.Library()


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.filter
def filesize(value):
    return os.path.getsize(value)
    # # value = ing(value)
    # if result < 512000:
    #     result = result / 1024.0
    #     ext = 'kb'
    # elif result < 4194304000:
    #     result = result / 1048576.0
    #     ext = 'mb'
    # else:
    #     result = result / 1073741824.0
    #     ext = 'gb'
    # return '%s %s' % (str(round(result, 2)), ext)

