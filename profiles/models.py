from django.db import models
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = "profile"
    )
    image = ImageField(upload_to='profiles')
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a new UserProfile() obj when new Django user is created """
    if created:
        new_user = UserProfile.objects.create(user=instance)