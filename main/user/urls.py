from django.urls import path

from user.views import UserDetailView, UserProfileView, add_friends, Friends_request_listview

urlpatterns = [
    path('profile_setting/<str:username>', UserDetailView.as_view(), name='profile'),
    path('user/<str:username>', UserProfileView.as_view(), name='user_profile'),
    path('add_user/<str:user_to>', add_friends, name='add_friends'),
    path('friends_request', Friends_request_listview.as_view(), name='friends_request'),
]
