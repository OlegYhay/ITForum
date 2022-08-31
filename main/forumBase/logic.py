from django.db.models import Avg
from forumBase.models import TopicRaiting


def average_rating_topic(topic):
    result = TopicRaiting.objects.filter(Topic=topic).aggregate(result=Avg('Grade')).get('result')
    topic.AveregeRaiting = result
    topic.save()