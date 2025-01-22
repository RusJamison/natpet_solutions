from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile,User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance whenever a User is created.
    """
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for user: {instance.username}")