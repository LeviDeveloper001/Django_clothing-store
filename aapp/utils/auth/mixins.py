from typing import Any

from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.views.generic import View
from django.http import HttpRequest

from accounts.models import Profile

class AuthMixin(ContextMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context['user']=user
        context['is_auth'] = user.is_authenticated
        return context



class ProfileMixin(AuthMixin):
    request:HttpRequest
    profile_model=Profile
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile=self.profile_model.manager.get(user=self.request.user)
        else:
            profile=None 
        context['profile']=profile
        self.profile=profile
        return context
    
    def get_profile(self) -> Profile:
        if self.request.user.is_authenticated:
            return self.profile or Profile.manager.get(user=self.request.user)
        
        




