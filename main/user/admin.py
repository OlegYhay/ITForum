from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreateForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    model = CustomUser


@register(CustomUser)
class UserModel(admin.ModelAdmin):
    pass