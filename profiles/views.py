from typing import Any

from django.forms.models import BaseModelForm
from feed.models import Post
from .models import UserProfile
from django.shortcuts import render
from followers.models import Follower
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest as HttpRequest
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import DetailView, View, UpdateView
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# class UpdateProfile(LoginRequiredMixin, UpdateView):
#     template_name = 'profiles/update.html'
#     model = UserProfile
#     fields = ['image']
#     success_url="/"
    
    

class ProfileViewMe(LoginRequiredMixin,DetailView):
    http_method_names=['get']
    template_name='profiles/profileme.html'
    model = User
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        request = self.request
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.get_object()
        context=super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author = user).count()
        context['followers'] = Follower.objects.filter(following = user).count()
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
            
        return context    

class ProfileView(DetailView):
    http_method_names=['get']
    template_name='profiles/profile.html'
    model = User
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        request = self.request
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.get_object()
        context=super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author = user).count()
        context['followers'] = Follower.objects.filter(following = user).count()
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
            
        return context
class FollowView(LoginRequiredMixin,View):
    http_method_names=['post']
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        
        if 'action' not in data or 'username' not in data:
            return HttpResponseBadRequest('Missing data')
        
        try:
            other_user=User.objects.get(username=data['username'])
            
        except User.DoesNotExist:
            return HttpResponseBadRequest('Missing user')
            
        if data['action'] == 'follow':
            #Follow
            follower, created = Follower.objects.get_or_create(
                followed_by = request.user,
                following = other_user,
            )
        else:
            try:
                follower = Follower.objects.get(
                followed_by = request.user,
                following = other_user,
            )
            except Follower.DoesNotExist:
                follower = None 
            if follower:
                follower.delete()
            #UnFollow
        return JsonResponse({
            'success':True,
            'wording': "Unfollow" if data['action'] == 'follow' else 'Follow'
        })