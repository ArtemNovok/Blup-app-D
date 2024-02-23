from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length = 35, blank = False, null=False)
    text = models.CharField(max_length=240, blank = False, null=False)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    
    def __str__(self) -> str:
        return self.text