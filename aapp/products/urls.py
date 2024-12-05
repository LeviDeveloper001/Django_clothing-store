from django.urls import path
from . import views

app_name='products'
urlpatterns = [
    path('', views.BaseView.as_view(), name='home'), 
    path('add/', view=views.AddProductView.as_view(), name='add')
]

products_config = (urlpatterns, app_name)
