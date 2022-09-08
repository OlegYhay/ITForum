from django.urls import path

from user.views import UserDetailView, UserProfileView

urlpatterns = [
    path('profile_setting/<str:username>', UserDetailView.as_view(), name='profile'),
    path('user/<str:username>', UserProfileView.as_view(), name='user_profile'),
]
