from django.contrib import admin

# Register your models here.
from django.contrib.admin import register

from forumBase.models import Category, Topic, CommentTopic


@register(Category)
class CategoryModel(admin.ModelAdmin):
    pass

@register(Topic)
class TopicModel(admin.ModelAdmin):
    pass


@register(CommentTopic)
class CommentModel(admin.ModelAdmin):
    pass