from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.roungnakhone_hotel.models import Receptionist, Guest


@receiver(post_delete, sender=Receptionist)
def delete_receptionist(sender, instance, **kwargs):
    # Automatically delete the associated user when the Receptionist is deleted
    instance.user.delete()


@receiver(post_delete, sender=Guest)
def delete_guest(sender, instance, **kwargs):
    # Automatically delete the associated user when the Guest is deleted
    instance.user.delete()
