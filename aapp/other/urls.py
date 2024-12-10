from django.urls import path
from . import views

app_name='other'

urlpatterns = [
    path('for_sellers/', views.ForSellersPageView.as_view(), name='for_sellers'),
]

other_config = (urlpatterns, app_name)
