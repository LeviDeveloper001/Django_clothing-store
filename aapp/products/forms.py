from django import forms

from .models import Product, ProductImage


class AddProductForm(forms.ModelForm):
    image_1 = forms.ImageField()
    image_2 = forms.ImageField()
    image_3 = forms.ImageField()
    class Meta:
        model=Product
        fields = ('name', 'description', 'price')





