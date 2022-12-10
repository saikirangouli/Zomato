from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ZomatoApp.models import *
from .serializers import *
from datetime import datetime

@api_view(['GET'])
def dishes_list(request,restaurant_id):
    restaurant_object = Restaurant.objects.get(restaurant_id=restaurant_id)
    dishes= Dish.objects.filter(restaurant_name=restaurant_object)
    serializer = DishSerializer(dishes,many=True)
    return Response({'status':200,'payload':serializer.data})
# @api_view(['GET','POST'])
# def place_order(request):
#     if 'customer_login' in request.session:
#         user_name = request.session['customer_login']
#         user_object=Customer.objects.get(user_name=user_name)
#         cart_object = Cart.objects.filter(user_name=user_object)
#         cart_objects=CartSerializer(cart_object,many=True)
#         order_object=Order.objects.create(cart=)
#     return Response(cart_objects.data)


