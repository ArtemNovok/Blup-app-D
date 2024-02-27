from typing import Any
from .models import Post
from django.shortcuts import render
from django.http import HttpResponse
from followers.models import Follower
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest as HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView, CreateView, TemplateView, UpdateView

# Create your views here.

class HomePage(ListView):
    http_method_names = ["get"]
    template_name = "feed/homepage.html"
    model = Post
    context_object_name = "posts"
    queryset = Post.objects.all().order_by("-id")[:30]

class FollowedView(TemplateView):
    http_method_names = ['get']
    template_name = 'feed/followed.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            following = list(Follower.objects.filter(followed_by=self.request.user).values_list('following', flat=True))
            post = Post.objects.filter(author__in=following).order_by("-id")[:30]
        else:
            post = Post.objects.all().order_by("-id")[:30]
        context['posts'] = post
        return context

class DetailView(DetailView):
    http_method_names = ["get"]
    template_name = 'feed/detail.html'
    model = Post
    context_object_name = 'post'
    
class EditPost(LoginRequiredMixin, UpdateView):
    template_name = "feed/editpost.html"
    model = Post
    fields=['title', 'text']
    success_url = '/'
    
class CreatePost(LoginRequiredMixin, CreateView):
    template_name = 'feed/new_post.html'
    model = Post
    fields = ['title', 'text']
    success_url ='/'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form) -> HttpResponse:
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)
    def post (self, request, *args, **kwargs):
        post = Post.objects.create(
            title= request.POST.get('title'),
            text= request.POST.get('text'),
            author= request.user
        )
        
        return render(
            request,
            "includes/post.html",
            {
                "post":post,
                "read_more":True,
            },
            content_type='application/html'
        )