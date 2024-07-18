# Generated by Django 5.0.6 on 2024-06-30 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0006_censorinfo_remove_nextmodel_hotel_main_img_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='nextmodel',
            name='dircertficate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='director', to='projectApp.dirinfo'),
        ),
    ]
