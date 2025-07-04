# Generated by Django 5.2.1 on 2025-05-27 00:04

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('capacity', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_by_name', models.CharField(help_text="Nom de la personne/entite qui reserve (si pas d'utilisateur connecte)", max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('purpose', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'En attente'), ('CONFIRMED', 'Confirmee'), ('CANCELLED', 'Annulee')], default='PENDING', max_length=10)),
                ('admin_notes', models.TextField(blank=True, help_text="Notes pour l'administrateur", null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='Utilisateur qui a fait la reservation', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking.room')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
    ]
