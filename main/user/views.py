from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from user.models import CustomUser


class UserDetailView(UpdateView):
    model = CustomUser
    template_name = 'profile/profile_settings.html'
    fields = ['username', 'first_name', 'last_name', 'img']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.username != kwargs['username']:
            return HttpResponse(status=400)
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        _object = CustomUser.objects.get(username=self.kwargs['username'])
        return _object

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})
