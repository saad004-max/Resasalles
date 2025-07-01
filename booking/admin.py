from django.contrib import admin
<<<<<<< HEAD
from .models import Room, Booking, Equipment, Feedback
=======
from .models import Room, Booking
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
from django.utils.html import format_html # Pour afficher l'image de maniere securisee

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'photo_thumbnail')
    search_fields = ('name', 'description')
<<<<<<< HEAD
    list_filter = ('capacity',)
=======
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f

    def photo_thumbnail(self, obj):
        if obj.photo and hasattr(obj.photo, 'url'):
            return format_html('<img src="{}" width="100" height="auto" />', obj.photo.url)
        return "Pas d'image"
    photo_thumbnail.short_description = 'Aperçu Photo'

<<<<<<< HEAD
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'booking__room__name', 'comment')
    readonly_fields = ('user', 'booking', 'rating', 'comment', 'created_at')
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'booked_by_name', 'user', 'start_time', 'end_time', 'status', 'display_equipments','created_at')
    list_filter = ('status', 'room', 'start_time', 'equipments')
    search_fields = ('room__name', 'user__username', 'booked_by_name', 'purpose')
    actions = ['confirm_bookings', 'cancel_bookings']
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('equipments',)

    fieldsets = (
        (None, {
            'fields': ('room', 'user', 'booked_by_name', 'purpose', 'equipments')
=======
# ... BookingAdmin reste probablement le même ...
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'booked_by_name', 'user', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'room', 'start_time')
    search_fields = ('room__name', 'user__username', 'booked_by_name', 'purpose')
    actions = ['confirm_bookings', 'cancel_bookings']
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('room', 'user', 'booked_by_name', 'purpose')
>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
        }),
        ('Dates et Heures', {
            'fields': ('start_time', 'end_time')
        }),
        ('Statut et Administration', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
<<<<<<< HEAD
    def display_equipments(self, obj):
        return ", ".join([eq.name for eq in obj.equipments.all()])
    display_equipments.short_description = "Équipements"
    
=======

>>>>>>> e4d17d223318b24013b81ac6e05f3b9c6a0ad70f
    def confirm_bookings(self, request, queryset):
        queryset.update(status='CONFIRMED')
    confirm_bookings.short_description = "Confirmer les reservations selectionnees"

    def cancel_bookings(self, request, queryset):
        queryset.update(status='CANCELLED')
    cancel_bookings.short_description = "Annuler les reservations selectionnees"