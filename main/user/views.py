from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from user.models import CustomUser


class UserDetailView(UpdateView):
    model = CustomUser
    template_name = 'profile/profile_settings.html'
    fields = ['username', 'first_name', 'last_name', 'img']

    def get_object(self, queryset=None):
        _object = CustomUser.objects.get(username=self.kwargs['username'])
        return _object

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})
