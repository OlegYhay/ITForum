from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from user.models import CustomUser, FriendRequest


class UserDetailView(UpdateView):
    model = CustomUser
    template_name = 'profile/profile_settings.html'
    fields = ['username', 'first_name', 'last_name', 'CanMessageOnlyFriends', 'img']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.username != kwargs['username']:
            return HttpResponse(status=400)
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        _object = CustomUser.objects.get(username=self.kwargs['username'])
        return _object

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})


class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'profile/user_profile.html'
    context_object_name = 'user_view'

    def get_object(self, queryset=None):
        objectUser = get_user_model().objects.get(username=self.kwargs['username'])
        return objectUser

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user1 = self.get_object()
        query1 = user1.friends.all()
        query2 = user1.users_friends.all()
        if self.request.user == user1 or len(
                self.get_object().users_friends.filter(user=self.request.user, friend=user1)) != 0:
            isfriend = 'Да'
        else:
            isfriend = 'Нет'
        if len(self.request.user.from_user.filter(request_from=self.request.user, request_to=self.get_object())) != 0:
            isfriend = 'заявка'
        context['isfrined'] = isfriend
        context['friends_custom'] = query1.union(query2)
        return context


def add_friends(request, user_to):
    if request.method == 'POST':
        new_request = FriendRequest(
            request_from=request.user,
            request_to=CustomUser.objects.get(email=user_to),
            status=False,
        )
        new_request.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
