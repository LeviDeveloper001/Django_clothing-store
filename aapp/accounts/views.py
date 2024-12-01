from typing import Any

from django.forms.forms import BaseForm
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic import DetailView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, get_user_model, logout

from utils.general.mixins import GeneralMixin

from . import forms
from . import models

User=get_user_model()

def base_view(request):
    return render(request, 'accounts/index.html')


class CustomLoginView(GeneralMixin, LoginView):
    template_name='accounts/login.html'
    form_class=forms.AuthForm
    redirect_authenticated_user='home:home'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    

class CustomLogoutView(GeneralMixin, LogoutView):
    http_method_names = ["get", "post", "options"]
    def get(self, request:HttpRequest):
        logout(request)
        return redirect('accounts:login')
    # next_page='accounts:login'
    

class ProfileView(GeneralMixin, DetailView):
    template_name='accounts/profile.html'
    model:models.Profile=models.Profile
    context_object_name='profile'

    def get(self, request:HttpRequest, pk:int, *args, **kwargs):
        profile=self.model.manager.get(pk=pk)
        print(profile)
        return super().get(request)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print(context, type(context))

        # context[""] = 
        return context
    
        

class RegisterView(GeneralMixin, FormView):
    form_class=forms.CustomUserCreationForm
    template_name='accounts/register.html'

    def get_form(self, form_class: type | None = ...) -> BaseForm:
        return super().get_form(form_class)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        context = self.get_context_data(**context)
        return super().render_to_response(context, **response_kwargs)

    def get(self, request:HttpRequest):
        if (request.user.is_authenticated): return redirect('home:home')
        form = self.form_class()
        return self.render_to_response({'form':form})

    def post(self, request:HttpRequest):
        post_data=request.POST
        form = self.form_class(post_data)
        if form.is_valid():
            form.save()
            user=User.manager.get(username=post_data.get('username'))
            profile = models.Profile.manager.create(user=user)
            profile.save()
            return redirect('accounts:login')  # Перенаправление на страницу входа после успешной регистрации
        return self.render_to_response({'form':form})

