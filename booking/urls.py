from django.urls import path
from .views import (
    RoomListView, RoomDetailView, CreateBookingView, MyBookingsView,
<<<<<<< HEAD
    DashboardView,AdminRoomListView, AdminRoomCreateView, AdminRoomUpdateView,
    UserLoginView, UserLogoutView , register, BookingUpdateView, BookingDeleteView, CreateFeedbackView
=======
    AdminRoomListView, AdminRoomCreateView, AdminRoomUpdateView,
    UserLoginView, UserLogoutView , register
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
)

urlpatterns = [
    path('', RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('room/<int:room_pk>/book/', CreateBookingView.as_view(), name='create_booking_for_room'), # Route pour pre-remplir la salle
    path('book/', CreateBookingView.as_view(), name='create_booking'), # Route generique
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
<<<<<<< HEAD
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
=======
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f

    # URLs pour "l'admin" custom (optionnel, car Django Admin est puissant)
    path('app-admin/rooms/', AdminRoomListView.as_view(), name='admin_room_list'),
    path('app-admin/rooms/add/', AdminRoomCreateView.as_view(), name='admin_add_room'),
    path('app-admin/rooms/<int:pk>/edit/', AdminRoomUpdateView.as_view(), name='admin_edit_room'),

    # Auth (si on fait simple)
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
<<<<<<< HEAD
    path('booking/<int:pk>/modifier/', BookingUpdateView.as_view(), name='edit_booking'),
    path('booking/<int:pk>/supprimer/', BookingDeleteView.as_view(), name='delete_booking'),
    path('booking/<int:booking_pk>/feedback/', CreateFeedbackView.as_view(), name='leave_feedback'),
=======
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
]