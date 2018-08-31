from django import template
register = template.Library()

@register.filter
def index (value, arg):
    if len(value) > arg:
        return value[int(arg)]
    return ""

@register.filter
def split_str(value, arg):
    #print value + " " + arg
    #print value.split(arg)
    return value.split(arg)
#register.filter('index',)