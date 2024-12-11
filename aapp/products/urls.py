from django.urls import path
from . import views

app_name='products'
urlpatterns = [
    path('<int:page>/', views.ProductListView.as_view(), name='product_list'),
    # path('<int:page>'),
    path('add/', views.AddProductView.as_view(), name='add'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='detail'),
    path('my-shopping-cart/', views.ShoppingCartView.as_view(), name='shopping_cart'),
]

products_config = (urlpatterns, app_name)
