from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.request import HttpRequest as HttpRequest
from .models import Post
from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePage(ListView):
    http_method_names = ["get"]
    template_name = "feed/homepage.html"
    model = Post
    context_object_name = "posts"
    queryset = Post.objects.all().order_by("-id")[:30]

class DetailView(DetailView):
    http_method_names = ["get"]
    template_name = 'feed/detail.html'
    model = Post
    context_object_name = 'post'
    
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