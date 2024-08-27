# myapp/templatetags/my_filters.py
from django import template


register = template.Library()


@register.filter(name="has_error_messages")
def has_error_messages(messages):
    return any(message.tags == "error" for message in messages)
