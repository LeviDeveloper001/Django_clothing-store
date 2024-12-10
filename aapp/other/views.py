from django.shortcuts import render
from django.views.generic import TemplateView

from utils.general.mixins import GeneralMixin

class ForSellersPageView(GeneralMixin, TemplateView):
    template_name='other/for_sellers.html'
