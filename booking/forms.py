# booking/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
<<<<<<< HEAD
from .models import Booking, Room, Equipment, Feedback
=======
from .models import Booking, Room

>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BookingForm(forms.ModelForm):
<<<<<<< HEAD
    equipments = forms.ModelMultipleChoiceField(
    queryset=Equipment.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False,
    label="Équipements supplémentaires"
    )
    class Meta:
        model = Booking
        fields = ['room', 'booked_by_name', 'start_time', 'end_time', 'purpose', 'equipments']
=======
    class Meta:
        model = Booking
        fields = ['room', 'booked_by_name', 'start_time', 'end_time', 'purpose']
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'purpose': forms.Textarea(attrs={'rows': 3}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'booked_by_name': forms.TextInput(attrs={'placeholder': 'Votre nom ou departement'}),
        }

    def __init__(self, *args, **kwargs):
        initial_room = kwargs.pop('initial_room', None)
        super().__init__(*args, **kwargs)
        # Ces lignes sont specifiques au BookingForm et doivent rester ici
        if 'start_time' in self.fields: # Verification pour plus de robustesse
            self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        if 'end_time' in self.fields: # Verification pour plus de robustesse
            self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

        if initial_room:
            # S'assurer que le champ 'room' existe avant d'y acceder
            if 'room' in self.fields:
                self.fields['room'].initial = initial_room


class UserRegisterForm(UserCreationForm): # DOIT heriter de UserCreationForm
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    # PAS de methode __init__ ici, sauf si vous avez une raison TReS specifique
    # et que vous savez ce que vous faites.
<<<<<<< HEAD
    # Si vous avez copie le __init__ de BookingForm ici, supprimez-le.
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Partagez votre expérience...'}),
        }
        labels = {
            'rating': "Votre note (sur 5)",
            'comment': "Votre commentaire (optionnel)",
        }
=======
    # Si vous avez copie le __init__ de BookingForm ici, supprimez-le.
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
