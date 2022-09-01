from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import UpdateModelMixin

from apiv1.serializers import LikeDislikeSerializer
from forumBase.models import CommentTopic


class ViewModelSerializer(UpdateAPIView):
    serializer_class = LikeDislikeSerializer
    queryset = CommentTopic.objects.all()
