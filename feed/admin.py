from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmit(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmit)