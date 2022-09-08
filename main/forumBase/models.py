import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.urls import reverse

from user.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', null=False, default='Без наименование')
    forum = models.ForeignKey('Forum', on_delete=models.SET_NULL, null=True, blank=True, related_name='categories')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Forum(models.Model):
    name = models.CharField(max_length=200, verbose_name='Форум', null=False)

    def __str__(self):
        return self.name


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice = [
        ('Открыта', 1),
        ('Закрыта', 2),
        ('Решена', 3),
    ]
    name = models.CharField(max_length=200, verbose_name='Тема', null=False, default='Без темы')

    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics', null=False,
                                   verbose_name='Категория')
    Creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_topics', null=False,
                                verbose_name='Создатель')
    DateOfCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    Description = models.TextField(verbose_name='Описание', null=True)
    status = models.CharField(max_length=20, choices=choice, null=False, default=1)
    AveregeRaiting = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Средний рейтинг', default=0)

    class Meta:
        ordering = ['DateOfCreation']

    def __str__(self):
        return f'{self.name} - {self.Creator} - {self.DateOfCreation}'

    def get_absolute_url(self):
        return reverse('category', kwargs={'id': self.id, })


class TopicRaiting(models.Model):
    choice = [
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Пойдет'),
        (2, 'Плохо'),
        (1, 'Лучше не видеть!'),
    ]
    Topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False, related_name='rait')
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='raituser')
    Grade = models.PositiveSmallIntegerField(choices=choice, null=False, verbose_name='Оценка обсуждению')

    def save(self, *args, **kwargs):
        from forumBase.logic import average_rating_topic
        super().save(*args, **kwargs)
        average_rating_topic(self.Topic)


class TopicSubscribe(models.Model):
    Topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False)
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='topics')


class CommentTopic(models.Model):
    Topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False, verbose_name='Тема',
                              related_name='messagees')
    User = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default='profile delete',
                             related_name='comments')
    CommentText = models.TextField(verbose_name='Комментарий')
    CommentFather = models.ForeignKey('CommentTopic', on_delete=models.CASCADE, null=True, blank=True)
    DateOfComment = models.DateTimeField(auto_now_add=True)
    CommentLike = models.IntegerField(default=0)
    CommentDislike = models.IntegerField(default=0)

    class Meta:
        ordering = ['DateOfComment']

    def __str__(self):
        return f'{self.CommentText}'


class CommentLikes(models.Model):
    comment_id = models.ForeignKey('CommentTopic', on_delete=models.CASCADE, related_name='comment_likes')
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='users_likes')

    def __str__(self):
        return f'{self.user_id}_{self.comment_id}'


class CommentDislikes(models.Model):
    comment_id = models.ForeignKey('CommentTopic', on_delete=models.CASCADE, related_name='comment_dislikes')
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='users_dislikes')

    def __str__(self):
        return f'{self.user_id}_{self.comment_id}'
