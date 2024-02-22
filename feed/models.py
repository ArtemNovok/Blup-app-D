from django.db import models

# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length = 35, blank = False, null=False)
    text = models.CharField(max_length=240, blank = False, null=False)
    date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return self.text