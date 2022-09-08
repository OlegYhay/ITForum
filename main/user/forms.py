from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import forms
from django.forms import ModelForm

from .models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)