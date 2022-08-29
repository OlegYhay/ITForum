from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from user.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', null=False, default='Без наименование')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Forum(models.Model):
    name = models.CharField(max_length=200, verbose_name='Форум',null=False)

class Topic(models.Model):
    name = models.CharField(max_length=200, verbose_name='Тема', null=False, default='Без темы')
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics', null=False,
                                   verbose_name='Категория')
    Creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_topics', null=False,
                                verbose_name='Создатель')
    DateOfCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    Description = models.TextField(verbose_name='Описание', null=True)

    class Meta:
        ordering = ['DateOfCreation']

    def __str__(self):
        return f'{self.name} - {self.Creator} - {self.DateOfCreation}'


class TopicRaiting(models.Model):
    choice = [
        ('Nice', 5),
        ('Good', 4),
        ('Middling', 3),
        ('Bad', 2),
        ('Terrible', 1),
    ]
    Topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False)
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    Grade = models.PositiveSmallIntegerField(choices=choice, null=False)


class TopicSubscribe(models.Model):
    Topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False)
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)


class CommentTopic(models.Model):
    Topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False, verbose_name='Тема',related_name='messagees')
    User = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default='profile delete')
    CommentText = models.TextField(verbose_name='Комментарий')
    CommentFather = models.ForeignKey('CommentTopic', on_delete=models.CASCADE, null=True,blank=True)
    DateOfComment = models.DateTimeField(auto_now_add=True)
    CommentLike = models.PositiveIntegerField(default=0)
    CommentDislike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.CommentText}'

    def getcountlike(self):
        return self.CommentLike

    def getcountdislike(self):
        return self.CommentDislike
