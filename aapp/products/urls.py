from django.urls import path
from . import views

app_name='products'
urlpatterns = [
    path('<int:page>/', views.ProductListView.as_view(), name='product_list'),
    # path('<int:page>'),
    path('add/', view=views.AddProductView.as_view(), name='add'),
    path('detail/<int:pk>', view=views.ProductDetailView.as_view(), name='detail')
]

products_config = (urlpatterns, app_name)
