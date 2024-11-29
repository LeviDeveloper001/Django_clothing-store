from django.urls import path
from . import views

app_name='accounts'
accounts_urlpatterns = [
    path('', views.base_view),
]

accounts_config = (accounts_urlpatterns, app_name)

