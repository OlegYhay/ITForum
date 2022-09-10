from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, Subquery
from django.shortcuts import render, redirect
import datetime
# Create your views here.
from django.urls import reverse_lazy, NoReverseMatch
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from forumBase.forms import ModelComment, ModelRating, ModelLikeDislike
from forumBase.logic import likes_count, dislikes_count
from forumBase.models import Category, Forum, Topic, CommentTopic, TopicRaiting, CommentLikes, CommentDislikes


class Home(ListView):
    model = Forum
    template_name = 'pages/home.html'
    context_object_name = 'forums'


class Topics(ListView):
    model = Topic
    template_name = 'pages/category.html'
    context_object_name = 'topicss'
    paginate_by = 12

    def get_queryset(self):
        Result = Topic.objects.filter(CategoryId=self.kwargs['pk']).annotate(
            lastmessage=Max('messagees__DateOfComment')).order_by('-DateOfCreation')
        if Result.count() == 0:
            return 'Error'
        return Result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Topics, self).get_context_data(**kwargs)
        if not isinstance(context['topicss'], str):
            context['category'] = context['topicss'][0].CategoryId
        else:
            context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context


class TopicDetail(DetailView):
    model = Topic
    template_name = 'pages/Topic.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['comment_form'] = ModelComment(instance=self.request.user)
            context['rating_form'] = ModelRating(instance=self.request.user)
            # don't use
            # context['like_form'] = ModelLikeDislike(instance=self.request.user)
            rait = TopicRaiting.objects.filter(User=self.request.user, Topic=self.get_object())
            if rait.count() == 0:
                context['rait'] = True
            else:
                context['rait'] = False
        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # create new comment
            if self.request.POST.get('form') == 'comment':
                try:
                    Father = CommentTopic.objects.get(pk=self.request.POST.get('parent_id'))
                    new_comment = CommentTopic(
                        Topic=self.get_object(),
                        User=self.request.user,
                        CommentText=request.POST.get('CommentText'),
                        DateOfComment=datetime.datetime.now(),
                        CommentLike=0,
                        CommentFather=Father,
                        CommentDislike=0,
                    )
                    new_comment.save()
                except:
                    Father = ''
                    new_comment = CommentTopic(
                        Topic=self.get_object(),
                        User=self.request.user,
                        CommentText=request.POST.get('CommentText'),
                        DateOfComment=datetime.datetime.now(),
                        CommentLike=0,
                        CommentDislike=0,
                    )
                new_comment.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'),
                                error_rait=False)
            # create new rating form

            new_TopicRaiting = TopicRaiting.objects.create(
                User=self.request.user,
                Topic=self.get_object(),
                Grade=self.request.POST.get('Grade'),
            )
            new_TopicRaiting.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class CreateTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = 'pages/create_topic.html'
    fields = ['name', 'Description']

    def form_valid(self, form):
        category = Category.objects.get(pk=self.kwargs['group'])
        form.instance.CategoryId = category
        form.instance.Creator = self.request.user
        return super(CreateTopicView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('topic', kwargs={'group': self.kwargs['group'], 'pk': self.object.pk})


class RulesTempalateView(TemplateView):
    template_name = 'pages/SiteRules.html'


def like_set(request, pk):
    if request.method == 'POST':
        try:
            likes = CommentLikes.objects.get(comment_id=pk, user_id=request.user)
            likes.delete()
        except:
            likes = CommentLikes.objects.create(
                comment_id=CommentTopic.objects.get(pk=pk),
                user_id=request.user,
            )
            likes.save()
        likes_count(likes.comment_id)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def dislike_set(request, pk):
    if request.method == 'POST':
        try:
            dislikes = CommentDislikes.objects.get(comment_id=pk, user_id=request.user)
            dislikes.delete()
        except:
            dislikes = CommentDislikes.objects.create(
                comment_id=CommentTopic.objects.get(pk=pk),
                user_id=request.user,
            )
            dislikes.save()
        dislikes_count(dislikes.comment_id)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
