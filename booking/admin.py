from django.contrib import admin
from .models import Room, Booking
from django.utils.html import format_html # Pour afficher l'image de maniere securisee

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'photo_thumbnail')
    search_fields = ('name', 'description')

    def photo_thumbnail(self, obj):
        if obj.photo and hasattr(obj.photo, 'url'):
            return format_html('<img src="{}" width="100" height="auto" />', obj.photo.url)
        return "Pas d'image"
    photo_thumbnail.short_description = 'Aperçu Photo'

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

    def confirm_bookings(self, request, queryset):
        queryset.update(status='CONFIRMED')
    confirm_bookings.short_description = "Confirmer les reservations selectionnees"

    def cancel_bookings(self, request, queryset):
        queryset.update(status='CANCELLED')
    cancel_bookings.short_description = "Annuler les reservations selectionnees"