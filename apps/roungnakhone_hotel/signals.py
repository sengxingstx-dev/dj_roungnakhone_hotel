from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, Payment


@receiver(post_save, sender=Reservation)
def update_room_status_on_booking(sender, instance, created, **kwargs):
    if created:
        print('Triggered Reservation signal...')
        # Calculate the total price
        nights = (instance.check_out_date - instance.check_in_date).days
        room = instance.room
        instance.total_price = nights * room.price
        instance.save()

        # Set the room available to False
        room.available = False
        room.save()


@receiver(post_delete, sender=Reservation)
def update_room_status_on_checkout(sender, instance, **kwargs):
    print('Triggered room post_delete...')
    room = instance.room
    room.available = True
    room.save()


@receiver(post_delete, sender=Payment)
def delete_payment(sender, instance, **kwargs):
    if instance.payment_slip:
        instance.payment_slip.delete(save=False)
