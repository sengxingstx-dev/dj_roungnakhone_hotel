from django.shortcuts import redirect


def guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        guest = request.guest
        if guest is None and request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)

    return wrapper


def receptionist_required(view_func):
    def wrapper(request, *args, **kwargs):
        receptionist = request.receptionist
        if receptionist is None:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper
