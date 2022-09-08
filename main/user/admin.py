from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreateForm, CustomUserChangeForm
from .models import CustomUser, Friends_user,FriendRequest



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    model = CustomUser


@register(CustomUser)
class CustomUserModel(admin.ModelAdmin):
    pass

admin.site.register(Friends_user)
admin.site.register(FriendRequest)