from django import forms
from django.core.exceptions import ValidationError

from .models import Product, ProductImage, ShoppingCart, ShoppingCartProduct


class AddProductForm(forms.ModelForm):
    image_1 = forms.ImageField()
    image_2 = forms.ImageField()
    image_3 = forms.ImageField()
    class Meta:
        model=Product
        fields = ('name', 'description', 'price')


def natural_int_validator(value:int):
    if not (isinstance(value, int) and value>0):
        raise ValidationError(f'"{value}"(type={type(value)}) не является натуральным числом')

class AddShoppingCartProduct(forms.Form):
    count=forms.IntegerField(required=True, validators=[natural_int_validator], initial=1)
    # hidden_field = forms.IntegerField(widget=forms.HiddenInput(), initial='значение')
    fields=('count', 'product_id')
    def is_valid(self):
        return super().is_valid()
    



