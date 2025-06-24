from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Pour la gestion des permissions
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Room, Booking
from .forms import BookingForm, RoomForm, UserRegisterForm # RoomForm ici est pour l'exemple, l'admin Django est plus puissant

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