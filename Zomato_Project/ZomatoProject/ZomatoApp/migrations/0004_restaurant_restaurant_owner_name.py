# Generated by Django 4.1 on 2022-09-01 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ZomatoApp', '0003_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='restaurant_owner_name',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ZomatoApp.customer'),
        ),
    ]
