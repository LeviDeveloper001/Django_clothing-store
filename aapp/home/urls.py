from django.urls import path
from . import views

app_name='home'

home_urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]


home_config = (home_urlpatterns, app_name)

