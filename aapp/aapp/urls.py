"""
URL configuration for aapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts.urls import accounts_config
from home.urls import home_config
from products.urls import products_config
from other.urls import other_config

urlpatterns = [ 
    path('', include(home_config, namespace='home')),
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_config, namespace='users')),
    path('products/', include(products_config, namespace='products'), name='products'),
    path('other/', include(other_config, namespace='other'))
]
