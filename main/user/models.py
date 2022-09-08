from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from forumBase.models import CommentTopic


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='email address', unique=True)
    img = models.ImageField(upload_to='userImg/', verbose_name='Аватарка')
    registration_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserModel()
    CanMessageOnlyFriends = models.BooleanField(default=False, verbose_name='Сообщения могут писать только друзья')

    def __str__(self):
        return self.email

    def count_message(self):
        return CommentTopic.objects.filter(User=self.pk).count()


class Friends_user(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users_friends')


class FriendRequest(models.Model):
    request_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    request_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    status = models.BooleanField(verbose_name='Заявка принята', default=False)


class UserChat(models.Model):
    members = models.ManyToManyField(get_user_model(), related_name='user_chats')


class Message(models.Model):
    chat = models.ForeignKey(UserChat, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    message = models.TextField('Сообщение')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message
