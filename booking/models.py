from django.db import models
from django.contrib.auth.models import User
# from cloudinary.models import CloudinaryField # Supprimer ou commenter
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    # Utilisez ImageField pour le stockage local
    photo = models.ImageField(upload_to='room_photos/', blank=True, null=True)
    # 'upload_to' specifie le sous-dossier dans MEDIA_ROOT où les photos des salles seront sauvegardees.
    
    
    def __str__(self):
        return self.name
class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"

    def __str__(self):
        return self.name
# ... Le reste du modele Booking reste inchange ...
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmee'),
        ('CANCELLED', 'Annulee'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Utilisateur qui a fait la reservation")
    booked_by_name = models.CharField(max_length=100, help_text="Nom de la personne/entite qui reserve (si pas d'utilisateur connecte)")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.TextField(blank=True, null=True)
    equipments = models.ManyToManyField(Equipment, blank=True, help_text="Équipements sélectionnés pour cette réservation")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, null=True, help_text="Notes pour l'administrateur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation pour {self.room.name} par {self.booked_by_name} de {self.start_time.strftime('%Y-%m-%d %H:%M')} à {self.end_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("L'heure de fin doit être apres l'heure de debut.")
        if not self.pk and self.start_time <= timezone.now():
            raise ValidationError("La date de debut de la reservation ne peut pas être dans le passe.")
        
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(status='CANCELLED')

        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError(
                f"Cette salle est deje reservee pendant la periode demandee. Reservations existantes: {', '.join([str(b.start_time.strftime('%H:%M')) + '-' + str(b.end_time.strftime('%H:%M')) for b in overlapping_bookings])}"
            )

    def get_absolute_url(self):
        return reverse('booking_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['start_time']
class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='feedback', help_text="Réservation associée à cet avis")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Utilisateur qui a laissé l'avis")
    rating = models.IntegerField(choices=RATING_CHOICES, help_text="Note de 1 à 5")
    comment = models.TextField(blank=True, null=True, help_text="Commentaire de l'utilisateur")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        ordering = ['-created_at']

    def __str__(self):
        return f"Avis de {self.user.username} pour la réservation #{self.booking.id} ({self.rating} étoiles)"
