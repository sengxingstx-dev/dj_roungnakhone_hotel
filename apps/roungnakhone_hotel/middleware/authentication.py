from apps.roungnakhone_hotel.models import Guest, Receptionist


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        guest = None
        receptionist = None

        if user.is_authenticated:
            if not user.is_superuser and not user.is_staff:
                # User is not a superuser or staff, hence potentially a guest
                guest = Guest.objects.filter(user=user).first()
            else:
                # User is a superuser or staff, hence potentially a receptionist
                receptionist = Receptionist.objects.filter(user=user).first()

        request.guest = guest  # Attach guest object to request for easy access in views
        request.receptionist = (
            receptionist  # Attach receptionist object to request for easy access in views
        )

        response = self.get_response(request)
        return response
