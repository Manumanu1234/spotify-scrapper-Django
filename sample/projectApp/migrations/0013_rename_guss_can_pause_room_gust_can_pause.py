# Generated by Django 5.0.6 on 2024-07-10 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0012_room_delete_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='guss_can_pause',
            new_name='gust_can_pause',
        ),
    ]
