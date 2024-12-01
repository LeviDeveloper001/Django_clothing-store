from django.urls import path
from . import views

app_name='accounts'
accounts_urlpatterns = [
    path('', views.base_view),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
]

accounts_config = (accounts_urlpatterns, app_name)

