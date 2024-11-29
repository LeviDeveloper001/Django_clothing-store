from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from . import models

User=get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def save(self, commit: bool = ...) -> Any:
        saved = super().save(commit)
        return saved


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AuthForm(AuthenticationForm):
    pass





