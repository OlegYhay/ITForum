from django.db.models import Count, Max, Subquery
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from forumBase.models import Category, Forum, Topic


class Home(ListView):
    model = Forum
    template_name = 'pages/home.html'
    context_object_name = 'forums'


class Topics(ListView):
    model = Topic
    template_name = 'pages/category.html'
    context_object_name = 'topicss'

    def get_queryset(self):
        return Topic.objects.filter(CategoryId=self.kwargs['pk']).annotate(
            lastmessage=Max('messagees__DateOfComment')
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Topics, self).get_context_data(**kwargs)
        context['category'] = context['topicss'][0].CategoryId
        return context
