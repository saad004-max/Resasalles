from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Pour la gestion des permissions
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Room, Booking, Equipment, Feedback
from .forms import BookingForm, RoomForm, UserRegisterForm, FeedbackForm # RoomForm ici est pour l'exemple, l'admin Django est plus puissant
from django.views.generic.edit import DeleteView
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
# Vue pour afficher la liste des salles
class RoomListView(ListView):
    model = Room
    template_name = 'booking/room_list.html'
    context_object_name = 'rooms'

# Vue pour afficher les details d'une salle et le formulaire de reservation
class RoomDetailView(DetailView):
    model = Room
    template_name = 'booking/room_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        context['booking_form'] = BookingForm(initial_room=room) # Pre-remplir la salle
        # Recuperer les reservations confirmees et en attente pour cette salle et pour le futur
        context['bookings'] = Booking.objects.filter(
            room=room,
            status__in=['PENDING', 'CONFIRMED'],
            end_time__gte=timezone.now()
        ).order_by('start_time')
        # Recuperer les avis pour cette salle
        context['feedbacks'] = Feedback.objects.filter(booking__room=room).order_by('-created_at')
        # Calculer la note moyenne
        avg_rating = context['feedbacks'].aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = round(avg_rating, 1) if avg_rating else None

        return context

# Vue pour creer une reservation
class CreateBookingView(LoginRequiredMixin, CreateView): # LoginRequiredMixin impose la connexion
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html' # Un template generique pour le formulaire de reservation

    def form_valid(self, form):
        form.instance.user = self.request.user # Assigner l'utilisateur connecte
        # booked_by_name est dejà dans le formulaire, mais on pourrait le forcer:
        # form.instance.booked_by_name = self.request.user.get_full_name() or self.request.user.username
        messages.success(self.request, "Votre demande de reservation a ete enregistree. Elle est en attente de confirmation.")
        # La validation des chevauchements est geree dans Booking.clean()
        return super().form_valid(form)

    def get_success_url(self):
        # Rediriger vers la page de detail de la salle apres la reservation
        return reverse_lazy('room_detail', kwargs={'pk': self.object.room.pk})

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get('room_id')
        if room_id:
            try:
                initial['room'] = Room.objects.get(pk=room_id)
            except Room.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Faire une reservation"
        room_id = self.request.GET.get('room_id')
        if room_id:
             try:
                context['room_being_booked'] = Room.objects.get(pk=room_id)
             except Room.DoesNotExist:
                pass
        return context

# Vue pour que l'utilisateur voie ses propres reservations
class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-start_time')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'booking/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Tableau de Bord"

        # Total counts
        context['total_bookings'] = Booking.objects.count()
        context['total_users'] = User.objects.count()
        context['total_rooms'] = Room.objects.count()

        # Booking status breakdown
        context['confirmed_bookings'] = Booking.objects.filter(status='CONFIRMED').count()
        context['pending_bookings'] = Booking.objects.filter(status='PENDING').count()
        context['cancelled_bookings'] = Booking.objects.filter(status='CANCELLED').count()

        # Most popular room
        most_booked_room = Booking.objects.values('room__name').annotate(count=Count('room')).order_by('-count').first()
        context['most_booked_room'] = most_booked_room

        # Most requested equipment
        most_requested_equipment = Booking.objects.filter(equipments__isnull=False).values('equipments__name').annotate(count=Count('equipments')).order_by('-count').first()
        context['most_requested_equipment'] = most_requested_equipment

        # Recent bookings
        context['recent_bookings'] = Booking.objects.order_by('-created_at')[:5]
        # Feedback stats
        context['total_feedbacks'] = Feedback.objects.count()
        avg_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
        context['average_rating_overall'] = round(avg_rating, 2) if avg_rating else 'N/A'
        context['recent_feedbacks'] = Feedback.objects.select_related('user', 'booking__room').order_by('-created_at')[:5]

        return context

        

# Vues pour l'admin (si on veut une interface en dehors de Django Admin)
# La plupart des fonctionnalites admin (ajouter salle, modifier photo, confirmer/modifier resa)
# sont tres bien gerees par Django Admin.
# Si vous voulez une interface custom pour l'admin:

class AdminRoomListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Room
    template_name = 'booking/admin_room_list.html' # A creer
    context_object_name = 'rooms'

    def test_func(self):
        return self.request.user.is_staff

class AdminRoomCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'booking/admin_room_form.html' # A creer
    success_url = reverse_lazy('admin_room_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, f"Salle '{form.instance.name}' ajoutee avec succes.")
        return super().form_valid(form)


class AdminRoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'booking/admin_room_form.html' # A creer
    success_url = reverse_lazy('admin_room_list')

    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, f"Salle '{form.instance.name}' modifiee avec succes.")
        return super().form_valid(form)

# Les vues pour confirmer/modifier les infos d'une reservation
# sont typiquement gerees dans l'interface Django Admin.
# L'admin peut y changer le statut, les dates, etc.
# BookingAdmin dans admin.py est là pour ça.

# Exemple simple pour la connexion/deconnexion si vous n'utilisez pas django-allauth etc.
from django.contrib.auth import views as auth_views

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # Sauvegarde l'utilisateur
            # Optionnel : Connecter l'utilisateur automatiquement apres l'inscription
            # login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte cree pour {username} ! Vous pouvez maintenant vous connecter.')
            return redirect('login') # Rediriger vers la page de connexion
    else:
        form = UserRegisterForm()
    return render(request, 'booking/register.html', {'form': form, 'page_title': "S'inscrire"})


class UserLoginView(auth_views.LoginView):
    template_name = 'booking/login.html' # A creer

class UserLogoutView(auth_views.LogoutView):
    # Pas de template necessaire si LOGOUT_REDIRECT_URL est defini
    pass
class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'  # On peut réutiliser le même formulaire

    def get_success_url(self):
        messages.success(self.request, "Votre réservation a été mise à jour.")
        return reverse_lazy('my_bookings')

    def test_func(self):
        booking = self.get_object()
        return booking.user == self.request.user  # Ne permettre que la modification par le créateur


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'booking/booking_confirm_delete.html'
    success_url = reverse_lazy('my_bookings')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Réservation supprimée avec succès.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        booking = self.get_object()
        return booking.user == self.request.user
class CreateFeedbackView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'booking/feedback_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.booking = get_object_or_404(Booking, pk=self.kwargs.get('booking_pk'))
        # Verifier que l'utilisateur est bien le proprietaire de la reservation
        if self.booking.user != self.request.user:
            return HttpResponseForbidden("Vous n'êtes pas autorisé à laisser un avis pour cette réservation.")
        # Verifier que la reservation est terminee
        if self.booking.end_time > timezone.now():
            messages.error(request, "Vous ne pouvez laisser un avis qu'après la fin de la réservation.")
            return redirect('my_bookings')
        # Verifier qu'un avis n'existe pas dejà
        if hasattr(self.booking, 'feedback'):
             messages.error(request, "Vous avez déjà laissé un avis pour cette réservation.")
             return redirect('my_bookings')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Laisser un avis pour {self.booking.room.name}"
        context['booking'] = self.booking
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.booking = self.booking
        messages.success(self.request, "Merci ! Votre avis a été enregistré.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_bookings')
