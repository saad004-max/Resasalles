# Generated by Django 4.2.21 on 2025-06-30 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_room_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium')], default='standard', max_length=10),
        ),
    ]
