from django import template
import os

register = template.Library()

@register.filter
def replace(value):
    print(value)
    return value.replace('/','jaimatadee')


def get_filename(value):
    return os.path.basename(value)



@register.filter(name='check_in_list')
def check_in_list(result1, item_to_check):
    print(result1,item_to_check)
    print(type(result1))
    print(item_to_check in result1)
    return item_to_check in result1
    
