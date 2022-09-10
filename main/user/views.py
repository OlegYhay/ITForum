from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, ListView, DeleteView

from user.models import CustomUser, FriendRequest, Friends_user
from user.tasks import send_friend_request


class UserDetailView(UpdateView):
    model = CustomUser
    template_name = 'profile/profile_settings.html'
    fields = ['username', 'first_name', 'last_name', 'CanMessageOnlyFriends', 'img']
    context_object_name = 'user_view'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.username != kwargs['username']:
            return HttpResponse(status=400)
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        _object = CustomUser.objects.get(username=self.kwargs['username'])
        return _object

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user1 = self.get_object()
        query1 = user1.friends.all()
        query2 = user1.users_friends.all()
        context['friends_custom'] = query1.union(query2)
        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})


class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'profile/user_profile.html'
    context_object_name = 'user_view'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() == self.request.user:
            return redirect(reverse('profile', kwargs={'username': self.request.user.username}))
        if self.request.user.is_anonymous:
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

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
        if len(FriendRequest.objects.filter(request_from=self.get_object(), request_to=self.request.user,
                                            status=False)) != 0:
            isfriend = 'принять'
        print(isfriend)
        context['isfrined'] = isfriend
        context['friends_custom'] = query1.union(query2)
        return context


def add_friends(request, user_to):
    if request.method == 'POST':
        request_to = CustomUser.objects.get(email=user_to)
        new_request = FriendRequest(
            request_from=request.user,
            request_to=request_to,
            status=False,
        )
        new_request.save()
        send_friend_request.delay(request.user.username, request_to.email)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class Friends_request_listview(ListView):
    model = FriendRequest
    context_object_name = 'requests'
    template_name = 'profile/friends_requests.html'

    def get_queryset(self):
        return FriendRequest.objects.filter(Q(request_to=self.request.user) & Q(status=False))

    def post(self, request, *args, **kwargs):
        if self.request.POST['action'] == 'add':
            friend = CustomUser.objects.get(email=self.request.POST['friend'])
            new_friend = Friends_user.objects.create(
                user=self.request.user,
                friend=friend
            )
            new_friend.save()
            friend_request = FriendRequest.objects.get(request_from=friend,
                                                       request_to=self.request.user)
            friend_request.status = True
            friend_request.save()

        elif self.request.POST['action'] == 'delete':
            friend = CustomUser.objects.get(email=self.request.POST['friend'])
            friend_request = FriendRequest.objects.get(request_from=friend,
                                                       request_to=self.request.user)
            friend_request.delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
