from typing import Any
from feed.models import Post
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import DetailView
# Create your views here.
class ProfileView(DetailView):
    http_method_names=['get']
    template_name='profiles/profile.html'
    model = User
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.get_object()
        context=super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author = user).count()
        return context