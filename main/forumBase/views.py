from django.db.models import Count, Max
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView

from forumBase.models import Category


class Home(ListView):
    model = Category
    template_name = 'pages/home.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all().annotate(count_message=Count('topics__messagees'),
                                               lastpub=Max('topics__DateOfCreation'))
