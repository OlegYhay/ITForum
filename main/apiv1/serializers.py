from rest_framework import serializers

from forumBase.models import CommentTopic


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Metal:
        model = CommentTopic
        fields = ['id', 'CommentLike', 'CommentDislike']
