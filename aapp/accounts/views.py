from typing import Any

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.forms.forms import BaseForm
from django.shortcuts import render, redirect # resolve_url
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic import DetailView, FormView, TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, get_user_model, logout

from utils.general.mixins import GeneralMixin

from . import forms
from . import models

User=get_user_model()

class BaseView(GeneralMixin, RedirectView):
    url='users:login'

def base_view(request:HttpRequest):
    return redirect('users:login')



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
        return redirect('users:login')
    # next_page='accounts:login'
    


class ProfileView(GeneralMixin, TemplateView):
    template_name='accounts/profile.html'
    model:models.Profile=models.Profile
    context_object_name='profile'

    def get_profile(self):
        user=self.request.user
        if not user.is_authenticated: return None
        profile = self.model.manager.get(user=user)
        return profile

    def get(self, request:HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated: return redirect('users:login')
        return super().get(request)
        
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_profile()
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
            return redirect('users:login')  # Перенаправление на страницу входа после успешной регистрации
        return self.render_to_response({'form':form})



class ChangeProfileView(GeneralMixin, FormView): 
    template_name='accounts/change_profile.html'
    form_class=forms.ChangeProfileForm
    success_url='../'
    model=models.Profile



    def get_success_url(self) -> str:
        return self.success_url

    def form_valid(self, form):
        # Сохраняем загруженное изображение в базе данных
        # user_image = form.save()  # Сохраняем объект UserImage
        return super().form_valid(form)

    def get_form(self, form_class: type | None = ...) -> BaseForm:
        if self.request.method=='POST':
            return self.form_class(
                self.request.POST,
                self.request.FILES
            )
        return self.form_class()

    def post(self, request:HttpRequest, *args, **kwargs):
        form:forms.ChangeProfileForm=self.get_form()
        post_data=request.POST
        files_data=request.FILES
        
        
        # print(files_data, len(files_data))
        if form.is_valid():
            # new_profile_image:InMemoryUploadedFile=files_data['profile_image']
            # user_profile:models.Profile=self.model.manager.get(user=request.user)
            profile:models.Profile=self.model.manager.get(user=request.user)
            print('\n\n\n\n\n',   profile.profile_image     ,'\n\n\n\n\n')
            for field in form.Meta.fields:
                if field in post_data:
                    profile.__setattr__(field, post_data.get(field))
                elif field in files_data:
                    file:InMemoryUploadedFile=files_data.get(field)
                    profile.__setattr__(field, file)
                    profile.profile_image
            profile.save()
            return redirect(self.success_url)

        else:
            print('form not valid')
        
        return super().post(request, *args, **kwargs)


