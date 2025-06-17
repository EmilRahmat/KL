from django import template
register = template.Library()

@register.filter
def dict(choices, value):
    return dict(choices).get(value)