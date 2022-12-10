# Generated by Django 4.1 on 2022-09-01 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ZomatoApp', '0004_restaurant_restaurant_owner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_owner_name',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='ZomatoApp.customer'),
        ),
    ]
