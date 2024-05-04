from django.db import models
from django.db.models import Sum
from .utils.files import (
    max_file_size_validator,
    validate_image_extension,
    receptionist_storage,
    guest_storage,
    room_storage,
    payment_storage,
)
from apps.account.models import Account


class Guest(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        # default='default_profiles/default.jpg',
        upload_to=guest_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user}'

    @classmethod
    def total_guests(cls):
        return cls.objects.count()


class Receptionist(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        # default='default_profiles/default.jpg',
        upload_to=receptionist_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user}'

    @classmethod
    def total_receptionists(cls):
        return cls.objects.count()


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.category_name


class Room(models.Model):
    room_image = models.ImageField(
        upload_to=room_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    number = models.CharField(max_length=15, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.number

    @classmethod
    def total_rooms(cls):
        return cls.objects.count()

    @classmethod
    def available_rooms(cls):
        return cls.objects.filter(available=True).count()


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.guest} booked for room: {self.room}'

    @classmethod
    def total_revenue(cls):
        return cls.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0

    @classmethod
    def total_bookings(cls):
        return cls.objects.count()


class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    payment_slip = models.ImageField(
        upload_to=payment_storage,
        null=True,
        blank=True,
        validators=[validate_image_extension, max_file_size_validator],
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.reservation} - {self.amount}'


class HotelInfo(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
