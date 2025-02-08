from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a UserProfile instance when a new User is created.

    Args:
        sender (Model): The model class that sent the signal.
        instance (User): The instance of the User model that was saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver that saves the UserProfile instance when a User is saved.

    Args:
        sender (Model): The model class that sent the signal.
        instance (User): The instance of the User model that was saved.
        **kwargs: Additional keyword arguments.
    """
    instance.userprofile.save()