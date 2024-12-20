from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('', views.base_view),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'), 
    path('profile/change/', views.ChangeProfileView.as_view(), name='change-profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
]

accounts_config = (urlpatterns, app_name)

