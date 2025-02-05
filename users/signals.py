from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance whenever a User is created.
    """
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for user: {instance.username}")
     #  user = instance
     #  profile = Profile.objects.create(
          # user = user,
          # username = user.username,
          # email = user.email,
          # name = user.first_name,
      # )

    # subject = 'Welcome to Natpet'
    # message = 'We are glad you are here'

    # send_mail(
    #    subject,
    #    message,
    #    settings.EMAIL_HOST_USER,
    #    [profile.email],
    #    fail_silently=False

    # )
