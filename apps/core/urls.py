from django.urls import path
from django.contrib.auth.decorators import login_required
from apps.account import views as account_views
from apps.roungnakhone_hotel import views


urlpatterns = [
    #
    # NOTE: Auth
    #
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('register/', account_views.register_view, name='register'),
    path('profile/', login_required(account_views.admin_profile_view), name='admin-profile'),
    #
    # NOTE: Dashboard
    #
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('manage-receptionists/', views.manage_receptionists, name='manage-receptionists'),
    path('manage-guests/', views.manage_guests, name='manage-guests'),
    path('manage-rooms/', views.manage_rooms, name='manage-rooms'),
    path('manage-categories/', views.manage_categories, name='manage-categories'),
    path('manage-reservations/', views.manage_reservations, name='manage-reservations'),
    path('manage-payments/', views.manage_payments, name='manage-payments'),
    path('icon-font-awesome/', views.icon_font_awesome, name='icon-font-awesome'),
    # -> Edit
    path('manage-rooms/edit/<int:pk>/', views.edit_room, name='edit-room'),
    path('manage-categories/edit/<int:pk>/', views.edit_category, name='edit-category'),
    # -> Delete
    path(
        'manage-receptionists/delete/<int:pk>/',
        views.delete_receptionist,
        name='delete-receptionist',
    ),
    path('manage-guests/delete/<int:pk>/', views.delete_guest, name='delete-guest'),
    path('manage-rooms/delete/<int:pk>/', views.delete_room, name='delete-room'),
    path('manage-categories/delete/<int:pk>/', views.delete_category, name='delete-category'),
    path(
        'manage-reservation/delete/<int:pk>/', views.delete_reservation, name='delete-reservation'
    ),
    path('manage-payment/delete/<int:pk>/', views.delete_payment, name='delete-payment'),
    # -> Exports
    path(
        'export-receptionists/csv/', views.export_receptionists_csv, name='export-receptionists-csv'
    ),
    path(
        'export-receptionists/excel/',
        views.export_receptionists_excel,
        name='export-receptionists-excel',
    ),
    path('export-guests/csv/', views.export_guests_csv, name='export-guests-csv'),
    path(
        'export-guests/excel/',
        views.export_guests_excel,
        name='export-guests-excel',
    ),
    path('export-rooms/csv/', views.export_rooms_csv, name='export-rooms-csv'),
    path(
        'export-rooms/excel/',
        views.export_rooms_excel,
        name='export-rooms-excel',
    ),
    path('export-reservations/csv/', views.export_reservations_csv, name='export-reservations-csv'),
    path(
        'export-reservations/excel/',
        views.export_reservations_excel,
        name='export-reservations-excel',
    ),
    #
    # NOTE: Home
    #
    path('', views.home, name='home'),
    path('user-profile/', login_required(account_views.user_profile_view), name='user-profile'),
    path(
        'edit-user-profile/<int:pk>/',
        login_required(account_views.edit_user_profile_view),
        name='edit-user-profile',
    ),
    path('accomodation/', views.accomodation, name='accomodation'),
    path('gallery/', views.gallery, name='gallery'),
    path('about-us/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
    #
    # NOTE: Reservation and Payment
    #
    path('reservation/<int:pk>/', login_required(views.reservation), name='reservation'),
    path('book-now/', views.book_now, name='book-now'),
    path('reservation/payment-receipt/<int:pk>/', views.payment_receipt, name='payment-receipt'),
    path(
        'export-payment-to-pdf/<int:pk>/', views.export_payment_to_pdf, name='export-payment-to-pdf'
    ),
    path('error-page/', views.error_page, name='error-page'),
]
