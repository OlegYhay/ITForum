from django.urls import path

from forumBase.views import Topics

urlpatterns = [
    path('category/<int:pk>', Topics.as_view(), name='category'),
]
