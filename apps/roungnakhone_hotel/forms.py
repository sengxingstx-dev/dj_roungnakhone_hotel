from django import forms

from .models import Room, Category, Reservation, Payment


class RoomForm(forms.ModelForm):
    room_image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Room
        fields = ['room_image', 'number', 'price', 'available', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_slip']
