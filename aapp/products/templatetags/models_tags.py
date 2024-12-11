from products import models

from typing import Any
from django import template

register = template.Library()



@register.filter(name="get_product_image")
def get_product_image(product:models.Product):
    image =  models.ProductImage.objects.filter(product=product).first().image
    path = f'../../../../../../../../{image}'
    return path




