from dataclasses import fields
from pyexpat import model
from ZomatoApp.models import *
from rest_framework import serializers


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'