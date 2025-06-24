from django.urls import path
from .views import (
    RoomListView, RoomDetailView, CreateBookingView, MyBookingsView,
    AdminRoomListView, AdminRoomCreateView, AdminRoomUpdateView,
    UserLoginView, UserLogoutView , register
)

urlpatterns = [
    path('', RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('room/<int:room_pk>/book/', CreateBookingView.as_view(), name='create_booking_for_room'), # Route pour pre-remplir la salle
    path('book/', CreateBookingView.as_view(), name='create_booking'), # Route generique
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),

    # URLs pour "l'admin" custom (optionnel, car Django Admin est puissant)
    path('app-admin/rooms/', AdminRoomListView.as_view(), name='admin_room_list'),
    path('app-admin/rooms/add/', AdminRoomCreateView.as_view(), name='admin_add_room'),
    path('app-admin/rooms/<int:pk>/edit/', AdminRoomUpdateView.as_view(), name='admin_edit_room'),

    # Auth (si on fait simple)
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]