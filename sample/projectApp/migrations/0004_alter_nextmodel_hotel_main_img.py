# Generated by Django 5.0.6 on 2024-06-29 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0003_nextmodel_hotel_main_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextmodel',
            name='hotel_Main_Img',
            field=models.ImageField(default='SOME STRING', upload_to='media/'),
        ),
    ]
