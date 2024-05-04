from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.roungnakhone_hotel.models import Receptionist, Guest, Reservation
from .forms import RegistrationForm, EditReceptionistProfileForm, EditGuestProfileForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect('dashboard')

            # Redirect to the next URL if it exists, otherwise redirect to a default URL
            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'account/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email').lower()
            phone = form.cleaned_data.get('phone')

            user = form.save()

            guest = Guest.objects.create(
                user=user,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
            )

            login(request, user)

            messages.success(request, 'Registration successful. You are now logged in.')

            if user.is_superuser or user.is_staff:
                return redirect('dashboard')

            return redirect('home')  # Replace 'dashboard' with the URL name of your dashboard view
    else:
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def admin_profile_view(request):
    user = request.user
    receptionist = Receptionist.objects.get(user=user)

    try:
        if request.method == 'POST':
            receptionist_form = EditReceptionistProfileForm(
                request.POST, request.FILES, instance=receptionist
            )

            if receptionist_form.is_valid():
                receptionist_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('admin-profile')
        else:
            receptionist_form = EditReceptionistProfileForm(instance=receptionist)

    except Receptionist.DoesNotExist:
        # Handle the case when the Receptionist does not exist for the current user
        receptionist = None
        print('Receptionist does not exist.')
    except Exception as e:
        print('Error:', str(e))

    context = {
        'user': user,
        'receptionist': receptionist,
        'receptionist_form': receptionist_form,
    }
    return render(request, 'dashboard/pages/pages-profile.html', context)


def user_profile_view(request):
    user = request.user
    guest = Guest.objects.filter(user=user).first()

    # Retrieve booking history for the current user's guest profile
    booking_history = Reservation.objects.filter(guest=guest).order_by('-updated_at')

    context = {'user': user, 'guest': guest, 'booking_history': booking_history}
    return render(request, 'account/profile.html', context)


def edit_user_profile_view(request, pk):
    user = request.user
    guest = Guest.objects.get(id=pk)

    try:
        if request.method == 'POST':

            guest_form = EditGuestProfileForm(request.POST, request.FILES, instance=guest)

            if guest_form.is_valid():
                guest_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('user-profile')
            else:
                print('Error: ', guest_form.errors)
        else:
            guest_form = EditGuestProfileForm(instance=guest)

    except Guest.DoesNotExist:
        # Handle the case when the Guest does not exist for the current user
        guest = None
        print('Guest does not exist.')
    except Exception as e:
        print('Error:', str(e))

    context = {'user': user, 'guest': guest}
    return render(request, 'account/edit-profile.html', context)
