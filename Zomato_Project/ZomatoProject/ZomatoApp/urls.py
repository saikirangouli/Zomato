from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('sign-up-page',signup,name='sign_up_page'),
    path('login-page',loginPage,name='login_page'),
    path('signup-details',signupdetails,name="signupdetails"),
    path('login-details',logindetails,name="logindetails"),
    path('edit-my-details',edit_restaurant_details,name="edit_restaurant_details"),
    path('add-dish',add_dish,name='add_dish'),
    path('logout',logout,name='logout'),
    path('search',search,name="search"),
    
    path('restaurant-details',restaurant_details,name="restaurantdetails"),
    path('change-password',password_change_page,name='change_password'),
    path('updated-password',updated_password,name='update_password'),
    path('show-dishes/<str:restaurant_id>',show_my_dishes,name='show_dishes'),
    path('delete_dish/<str:dish_id>',delete_dish,name='delete_dish'),
    path('selected_restaurant/<str:restaurant_id>',selected_restaurant,name='selected_restaurant'),
    path('add-to-cart/<str:dish_id>',add_to_cart,name='add_to_cart'),
    path('cart/',cart_page,name='cart_page'),
   path('cart/quantity-decrement/<str:dish_id>',quantity_decrement,name='quantity_decrement'),
    path('cart/quantity-increment/<str:dish_id>',quantity_increment,name='quantity_increment'),
    path('order-placed',order_placed,name='place_order'),
    path('my-orders/',my_orders,name='my_orders'),
    path('forgot-password',forgot_password,name='forgot_password'),
    path('send-reset-password',reset_password,name='sending_email'),
    path('date-wise-analytics',date_wise_analytics,name='date_wise_analytics_page'),
    path('date-wise-statistics',date_wise_analytics_results,name='date_wise_analytics'),
    path('delete-item/<str:cart_id>',delete_item_from_cart,name='delete_item'),
    path('date-wise-orders',date_wise_orders,name='date_wise_orders'),
    path('my-orders/search-order',search_for_order,name='search_for_order')
]