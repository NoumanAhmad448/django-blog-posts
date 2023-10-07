from django import template

register = template.Library()

@register.filter
def type(value):
    """type"""
    return type(value)

@register.filter
def split(value,args):
    """split the string to list"""
    return value.split(" ") if args.strip() == "" else value.split(args)


@register.simple_tag
def define(val=None):
  return val

@register.simple_tag
def current_url(request):
  return request.path

