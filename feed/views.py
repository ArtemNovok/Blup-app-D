from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
from django.views.generic import DetailView
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