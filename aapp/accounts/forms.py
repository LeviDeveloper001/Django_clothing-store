from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, SetPasswordMixin
from django.contrib.auth import get_user_model

from . import models

User=get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username=UsernameField(max_length=20, min_length=3, required=True, help_text=None)
    email = forms.EmailField(required=True, help_text=None)
    password1, password2= SetPasswordMixin.create_password_fields()
    password1:forms.Field
    password2:forms.Field
    password1.help_text=''
    password2.help_text=''

    def save(self, commit: bool = ...) -> Any:
        saved = super().save(commit)
        return saved


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    


class AuthForm(AuthenticationForm):
    pass





