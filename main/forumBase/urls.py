from django.urls import path

from forumBase.views import Topics, TopicDetail, CreateTopicView, like_set, dislike_set

urlpatterns = [
    path('category/<int:pk>', Topics.as_view(), name='category'),
    path('category/<int:group>/<uuid:pk>', TopicDetail.as_view(), name='topic'),
    path('category/<int:group>/create_topic', CreateTopicView.as_view(), name='createtopic'),
    path('add_like/<int:pk>/', like_set, name='like_set'),
    path('add_dislike/<int:pk>/', dislike_set, name='dislike_set'),
]
