from django.urls import path

from user.views import UserDetailView

urlpatterns = [
    path('profile_setting/<str:username>', UserDetailView.as_view(), name='profile')
]
