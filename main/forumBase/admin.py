from django.contrib import admin

# Register your models here.
from django.contrib.admin import register

from forumBase.models import Category, Topic, CommentTopic, Forum, TopicRaiting


class CategoryInLine(admin.TabularInline):
    model = Category


class TopicRaiting(admin.TabularInline):
    model = TopicRaiting


@register(Topic)
class TopicModel(admin.ModelAdmin):
    inlines = [TopicRaiting]


@register(CommentTopic)
class CommentModel(admin.ModelAdmin):
    pass


@register(Forum)
class ForumAdmin(admin.ModelAdmin):
    inlines = [CategoryInLine]
