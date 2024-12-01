from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from utils.general.mixins import GeneralMixin


class HomeView(GeneralMixin, TemplateView):
    template_name='home/home.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    

