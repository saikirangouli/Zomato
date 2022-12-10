from django.urls import path
from .views import *

urlpatterns=[
    path('dishes-list/<str:restaurant_id>',dishes_list,name='dishes_list'),
   # path('place-order/',place_order,name='place_order')

]