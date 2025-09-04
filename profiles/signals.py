from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a Profile instance whenever a new User instance is created.
    This function listens to the `post_save` signal emitted by the User model. When a new
    User instance is saved (created), it automatically creates a corresponding Profile
    instance with a default bio.
    Args:
        sender (Model): The model class that sent the signal (in this case, User).
        instance (User): The instance of the User model that was saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments passed by the signal.
    Note:
        This signal ensures that every User has an associated Profile created
        automatically upon registration.
    """
    if created:
        Profile.objects.create(
            user=instance,
            bio=f"This is {instance.username}'s profile."
        )



@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Tries to save the related Profile to ensure any changes to the User instance 
    are reflected in the Profile. If the Profile does not exist, it creates one 
    as a backup safety mechanism.
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(
            user=instance,
            bio=f"This is {instance.username}'s profile."
        )


