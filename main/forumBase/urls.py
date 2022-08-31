from django.urls import path

from forumBase.views import Topics, TopicDetail, CreateTopicView

urlpatterns = [
    path('category/<int:pk>', Topics.as_view(), name='category'),
    path('category/<int:group>/<uuid:pk>', TopicDetail.as_view(), name='topic'),
    path('category/<int:group>/create_topic', CreateTopicView.as_view(), name='createtopic'),
]

