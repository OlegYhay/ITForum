from django.db.models import Avg
from forumBase.models import TopicRaiting, CommentTopic, CommentLikes, CommentDislikes


def average_rating_topic(topic):
    result = TopicRaiting.objects.filter(Topic=topic).aggregate(result=Avg('Grade')).get('result')
    topic.AveregeRaiting = result
    topic.save()


def likes_count(comment):
    reesult = CommentLikes.objects.filter(comment_id=comment).count()
    print(reesult)
    comment.CommentLike = reesult
    comment.save()


def dislikes_count(comment):
    reesult = CommentDislikes.objects.filter(comment_id=comment).count()
    print(reesult)
    comment.CommentDislike = reesult
    comment.save()
