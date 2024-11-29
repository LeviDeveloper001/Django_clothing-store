from typing import Any

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, get_user_model

from . import forms
from . import models

User=get_user_model()

def base_view(request):
    return render(request, 'accounts/index.html')


class CustomLoginView(LoginView):
    template_name='accounts/login.html'
    form_class=forms.AuthForm
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    

class ProfileView(DetailView):
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
    
        

class RegisterView(View):
    def get(self, request):
        form = forms.CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request:HttpRequest):
        post_data=request.POST
        form = forms.CustomUserCreationForm(post_data)
        if form.is_valid():
            form.save()
            user=User.manager.get(username=post_data.get('username'))
            profile = models.Profile.manager.create(user=user)
            profile.save()
            return redirect('accounts:login')  # Перенаправление на страницу входа после успешной регистрации
        return render(request, 'accounts/register.html', {'form': form})

