# Generated by Django 5.0.6 on 2024-06-29 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0004_alter_nextmodel_hotel_main_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextmodel',
            name='hotel_Main_Img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
