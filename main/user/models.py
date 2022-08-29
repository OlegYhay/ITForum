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
    img = models.ImageField(upload_to='userImg/')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserModel()
    friends = models.ManyToManyField('self')

    def __str__(self):
        return self.email

    def count_message(self):
        return CommentTopic.objects.filter(User=self.pk).count()


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