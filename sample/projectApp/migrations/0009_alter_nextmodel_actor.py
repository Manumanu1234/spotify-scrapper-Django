# Generated by Django 5.0.6 on 2024-06-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0008_actor_nextmodel_actor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextmodel',
            name='actor',
            field=models.ManyToManyField(related_name='actorsdetails', to='projectApp.actor'),
        ),
    ]
