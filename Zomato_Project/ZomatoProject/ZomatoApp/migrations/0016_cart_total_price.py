# Generated by Django 4.1.1 on 2022-09-20 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZomatoApp', '0015_cart_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
