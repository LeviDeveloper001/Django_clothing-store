from typing import Any
from django import template

register = template.Library()



@register.filter(name="get")
def get(_dict:dict, key:Any):
    return _dict.get(key)

