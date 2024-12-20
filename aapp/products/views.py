from typing import Any
from django.forms.forms import BaseForm
from django.shortcuts import render, resolve_url, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.general.mixins import GeneralMixin

from . import forms, models

from accounts.models import Profile

class BaseView(GeneralMixin, TemplateView):
    template_name='products/base_view.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print(context)
        return context
    
class AddProductView(GeneralMixin, LoginRequiredMixin, FormView):
    form_class=forms.AddProductForm
    template_name='products/add_product.html'
    success_url='/'

    def form_valid(self, form:form_class):
        post_data, files_data = self.request.POST, self.request.FILES
        if self.request.method in ('POST', 'PUT'):
            user_profile=Profile.manager.get(user=self.request.user)
            product=models.Product(
                seller=user_profile,
                name=post_data['name'],
                description=post_data['description'],
                price=post_data['price']
            )
            form_is_valid=True
            product_images=[]
            for image_number in range(1, len(files_data)+1):
                image=files_data.get(f'image_{image_number}')
                if image_number>=15: break
                if not image:
                    if image_number<3:
                        return False    
                    break
                product_image=models.ProductImage(
                    image_number=image_number,
                    product=product, image=image
                )
                product_images.append(product_image)
            product.save()
            for image in product_images:
                image.save()
        return super().form_valid(form)
    

    def get_form(self, form_class: type | None = None) -> BaseForm:
        return super().get_form(form_class)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)


class ProductListView(GeneralMixin, ListView):
    template_name='products/product_list.html'
    images_model=models.ProductImage
    model=models.Product
    context_object_name='product_list'
    paginate_by=40
    # items_in_row = 

    def get_images_queryset(self, context:dict):
        product_list=context.get('product_list')
        product_images = dict()
        for product in product_list:
            main_image= self.images_model.objects.get(product=product, image_number=1).image
            product_images[product.pk] = main_image
        return product_images


    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['product_images']=self.get_images_queryset(context)
        return context
    

class ProductDetailView(GeneralMixin, DetailView, FormView):
    form_class=forms.AddShoppingCartProduct
    success_url='products:shopping_cart'
    template_name='products/product_detail.html'
    model=models.Product
    context_object_name='product' 

    def get_images_query_set(self, context:dict):
        return models.ProductImage.objects.filter(
            product=context['product']
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['product_images']=self.get_images_query_set(context)
        print(context)
        return context
    
    def get_success_url(self):
        return reverse(self.success_url)

    def valid_post_data(self):
        post_data=self.request.POST
        count, product_id = post_data.get('count'), post_data.get('product_id')
        try:
            count, product_id=int(count), int(product_id)
            product=models.Product.objects.get(id=product_id)
        except:
            return False
        return True
        
        

    def post(self, request, *args, **kwargs):
        post_data=request.POST
        form=self.get_form()
        if not form.is_valid() or not request.user.is_authenticated or not self.valid_post_data(): 
            return self.get(request)
        count=int(post_data.get('count'))
        product=models.Product(id=int(post_data.get('product_id')))
        profile=Profile.manager.get(user=request.user)
        shopping_cart=models.ShoppingCart.objects.get_or_create(buyer=profile)[0]
        
        for i in range(1, count+1):
            shopping_cart_product=models.ShoppingCartProduct(shopping_cart=shopping_cart, product=product)
            print(shopping_cart_product)
            shopping_cart_product.save()
        return redirect('products:shopping_cart')

        

        




class ShoppingCartView(GeneralMixin, LoginRequiredMixin, TemplateView):
    template_name='products/shopping_cart.html'
    model=models.ShoppingCart
    context_object_name='shopping_cart'
    products_model=models.ShoppingCartProduct
    products_context_queryset_name='products'
    queryset=None


    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    def get_products_queryset(self):
        return self.queryset or self.products_model.objects.filter(
            shopping_cart=self.get_shopping_cart()
        ).order_by('product__name')
    
    def get_shopping_cart(self):
        shopping_cart=self.model.objects.get_or_create(
            buyer=self.get_profile()
        )[0]
        return shopping_cart
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.context_object_name]=self.get_shopping_cart()
        context[self.products_context_queryset_name]=self.get_products_queryset()
        print(context)
        return context
    
    
    

