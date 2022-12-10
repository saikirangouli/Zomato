from datetime import datetime
from django.shortcuts import render
from .models import *
from django.contrib import messages
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
import sys
from .middleware import *
from django.core.mail import send_mail
import random
import array
from django.conf import settings
import pandas as pd

def home(request):
    return render(request,'base.html')

def signup(request):
    form = SignupForm()
    context={'form':form}
    return render(request,'Signup.html',context)

def signupdetails(request):
    if request.method == 'POST':
         form = SignupForm(request.POST)
         if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            user_name = form.cleaned_data.get('user_name')
            user_email = form.cleaned_data.get('user_email')
            user_type = form.cleaned_data.get('user_type')
            if Customer.objects.filter(user_name=user_name).exists():
                messages.error(request,'User name is already Exist')
                return render(request,'Signup.html',{'form':form})
            elif Customer.objects.filter(user_email=user_email).exists():
                messages.error(request,'User Email is already Exist')
                return render(request,'Signup.html',{'form':form})
            else:
                form.save()
            if user_type.is_customer:
                messages.success(request,'Details Saved Login Here')
                return render(request,'login.html')
            else:
                messages.success(request,'Details Saved Kindly add Your restaurant details')
                return render(request,'add_restaurant_details.html',{'user_name':user_name})
         else:
            messages.error(request,'Something went wrong')
            return render(request,'Signup.html',{'form':form})
       
        
       
        
    

def loginPage(request):
    return render(request,'login.html')


def logindetails(request):
    if 'customer_login' in request.session:
        user_name = request.session['customer_login']
        context={}
        context['user_name'] = user_name
        searching_objects = Restaurant.objects.all()
        context['restaurant_objects'] = searching_objects
        return render(request,'restaurant_selection.html',context)


    if 'restaurant_login' in request.session:
        context = {}
        user_name = request.session['restaurant_login']
        customer_object = Customer.objects.get(user_name=user_name)
        restaurant_details= Restaurant.objects.get(restaurant_owner_name=customer_object)
        context['restaurant_object']=restaurant_details
        context['user_name'] = user_name
        return render(request,'add_remove_dishes.html',context)


    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['user_password']
        context = {}
        context['user_name'] = user_name
        if len(user_name) == 0:
            messages.error(request,'User name cannot be empty')
            return render(request,'login.html')

        if len(password) == 0:
            messages.error(request,'Password cannot be empty')
            return render(request,'login.html')

        if Customer.objects.filter(user_name=user_name).exists():
            customer_object = Customer.objects.get(user_name=user_name)
            if customer_object.user_password == password and customer_object.user_type.is_customer:
                request.session['customer_login'] = user_name
                user_session_object = User_session.objects.create(user_session_id=customer_object)
                user_session_object.save()
                restaurant_list = Restaurant.objects.all()
                context['restaurant_objects'] = restaurant_list

                return render(request,'restaurant_selection.html',context)
            elif customer_object.user_password == password and customer_object.user_type.is_restaurant:
                context = {}
                request.session['restaurant_login'] = user_name
                restaurant_details= Restaurant.objects.get(restaurant_owner_name=customer_object)
                context['user_name'] = user_name
                context['restaurant_object'] = restaurant_details
                return render(request,'add_remove_dishes.html',context)
            else:
                messages.error(request,'Invalid Credentials')
                return render(request,'login.html')
        else:
            messages.error(request,'User Does not Exist Kindly Register Here !!!!')
            form = SignupForm()
            return render(request,'Signup.html',{'form':form})



def logout(request):
    try:

        if 'customer_login' in request.session:
            user_name = request.session['customer_login']
            user_object = Customer.objects.get(user_name=user_name)
            del request.session['customer_login']
            user_session_object = User_session.objects.get(user_session_id = user_object.customer_id)
            user_session_object.delete()

        if 'restaurant_login' in request.session:
            del request.session['restaurant_login']
    
        return render(request,'login.html')
    except:
        return render(request,'login.html')



def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
       
        context = {}
        user_name = request.session['customer_login']
        context['user_name'] = user_name
        searching_objects = Restaurant.objects.filter(restaurant_name__icontains=q)
        context['restaurant_objects'] = searching_objects
        return render(request,'restaurant_selection.html',context)

    else:
        searching_objects = Restaurant.objects.all()
        context['restaurant_objects'] = searching_objects
        return render(request,'restaurant_selection.html',context)






    

def add_dish(request):
    if request.method == 'POST':
        if 'restaurant_login' in request.session:
            user_name=request.session['restaurant_login']
        context={}
        context['user_name'] = user_name
        customer_object=Customer.objects.get(user_name=user_name)
        restaurant_object=Restaurant.objects.get(restaurant_owner_name=customer_object)

        dish_name = request.POST.get('dish_name')
        dish_price = request.POST.get('dish_price')
        dish_image = request.POST.get('dish_image')
        dish_object = Dish.objects.create(dish_name=dish_name,dish_price=dish_price,dish_image=dish_image,restaurant_name=restaurant_object)
        dish_object.save()
        context['restaurant_object'] = restaurant_object
        messages.info(request,'Dish is added Successfull add another if you want')
        return render(request,'add_remove_dishes.html',context)
    

def restaurant_details(request):
    if request.method == 'POST':
        restaurant_name = request.POST['restaurant_name']
        restaurant_address=request.POST['restaurant_address']
        restaurant_owner= request.POST['restaurant_owner']
        restaurant_owner=str(restaurant_owner)
        if Restaurant.objects.filter(restaurant_name=restaurant_name).exists():
            messages.error(request,'Restaurant name is already exists')
            return redirect()
        else:
            restaurant_owner_object = Customer.objects.get(user_name=restaurant_owner)
            restaurant_object = Restaurant(restaurant_name=restaurant_name,restaurant_adress=restaurant_address)
            restaurant_object.restaurant_owner_name = restaurant_owner_object
            restaurant_object.save()
            messages.success(request,'Your Details Saved Successfully Login Here')
            return render(request,'login.html')


def password_change_page(request):
    return render(request,'change_password.html')



#------------------------------------------------------update password-----------------------------------------------------

def updated_password(request):
    if request.method == 'POST':
        if 'customer_login' in request.session:
            user_name=request.session['customer_login']
        if 'restaurant_login' in request.session:
            user_name = request.session['restaurant_login']
        current_user_object=Customer.objects.get(user_name=user_name)
        current_user_password=current_user_object.user_password
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        new_password_again=request.POST['new_password_again']
        if current_user_password == current_password:
            if new_password == new_password_again:
                current_user_object.user_password = new_password
                current_user_object.save()
                messages.info(request,'Your password has been changed Successfully....Kindly login here')
                return render(request,'login.html')
            else:
                messages.error(request,'Passwords are not same')
                return redirect('change_password')

        else:
            messages.error(request,'You have Entered incorrect Current password')
            return redirect('change_password')


def show_my_dishes(request,restaurant_id):
    if 'restaurant_login' in request.session:

        context={}
        restaurant_object=Restaurant.objects.get(restaurant_id=restaurant_id)
        dish_objects= Dish.objects.filter(restaurant_name=restaurant_object)
        context['dish_objects'] = dish_objects
        return render(request,'restaurant_specific_dishes.html',context)
    else:
        messages.info(request,'Kindly login here')
        return redirect('login_page')


def delete_dish(request,dish_id):
    if 'restaurant_login' in request.session:
        user_name=request.session['restaurant_login']
    user_object=Customer.objects.get(user_name=user_name)
    restaurant_object=Restaurant.objects.get(restaurant_owner_name=user_object)
    dish_object=Dish.objects.get(dish_id=dish_id)
    dish_object.delete()
    return redirect('show_dishes',restaurant_id=restaurant_object.restaurant_id)


def selected_restaurant(request,restaurant_id):
    if 'customer_login' in request.session:

        context={}
        restaurant_object=Restaurant.objects.get(restaurant_id=restaurant_id)
        dishes_available=Dish.objects.filter(restaurant_name=restaurant_object)
        context['dishes_available'] = dishes_available
        context['restaurant_name'] = restaurant_object.restaurant_name
        return render(request,'customer_selected_dishes.html',context)
    else:
        messages.info(request,'Kindly  Login here')
        return redirect('login_page')



def cart_page(request):
    if 'customer_login' in request.session:
        user_name=request.session['customer_login']
   
   
        user_object = Customer.objects.get(user_name=user_name)
        context={}
        cart_objects=Cart.objects.filter(user_name=user_object,is_current=True)
        context['cart_objects'] = cart_objects
        return render(request,'cart.html',context)
    else:
        messages.info(request,'Kindly  Login here')
        return redirect('login_page')
        

def add_to_cart(request,dish_id):
    if 'customer_login' in request.session:
        user_name = request.session['customer_login']
    
    user_object = Customer.objects.get(user_name=user_name)
    dish_object=Dish.objects.get(dish_id=dish_id)

    order_date=datetime.now()
    order_date=order_date.strftime("%Y-%m-%d")
    user_cart=Cart.objects.filter(user_name=user_object,is_current=True)
    if user_cart.filter(dishes=dish_object,is_current=True).exists():

        cart_object=Cart.objects.get(dishes=dish_object)
        cart_object.quantity = cart_object.quantity + 1
        cart_object.total_price = cart_object.total_price + dish_object.dish_price
        cart_object.save()
    
    else:
        cart_object=Cart.objects.create(user_name=user_object,dishes=dish_object,total_price=dish_object.dish_price)

        cart_object.save()

    return redirect('cart_page')


def quantity_decrement(request,dish_id):
    if 'customer_login' in request.session:
        user_name = request.session['customer_login']
 
    
    user_object = Customer.objects.get(user_name=user_name)
    dish_object=Dish.objects.get(dish_id=dish_id)
    user_orders=Cart.objects.filter(user_name=user_object,is_current=True)
    order_object=user_orders.get(dishes=dish_object)
    if int(order_object.quantity) > 1:
        order_object.quantity = order_object.quantity - 1
        order_object.total_price = order_object.total_price - dish_object.dish_price
        order_object.save()
        return redirect('cart_page')
    else:
        order_object.delete()
        return redirect('cart_page')
    

def quantity_increment(request,dish_id):
    if 'customer_login' in request.session:
        user_name = request.session['customer_login']
   
    user_object = Customer.objects.get(user_name=user_name)
    dish_object=Dish.objects.get(dish_id=dish_id)
    user_orders=Cart.objects.filter(user_name=user_object,is_current = True)
    order_object=user_orders.get(dishes=dish_object)
    order_object.quantity = order_object.quantity + 1
    order_object.total_price = order_object.total_price + dish_object.dish_price
    order_object.save()
    return redirect('cart_page')


def order_placed(request):
    grand_total =0
    order_date=datetime.now()
    order_date=order_date.strftime('%Y-%m-%d')
    if 'customer_login' in request.session:
        user_name=request.session['customer_login']
    user_object=Customer.objects.get(user_name=user_name)
    cart_objects=Cart.objects.filter(user_name=user_object,is_current=True)
    if len(cart_objects) <= 0:
        messages.error(request,'The cart is empty add items to the cart')
        return redirect('cart_page')
    for item in cart_objects.values():
    
        grand_total += item['total_price']
    order_object=Order.objects.create(user_name=user_object,order_date=order_date,total_price=grand_total)
    for item in cart_objects:
        item.is_current = False
        item.save()
        order_object.cart.add(item)
    
    

   
    
    order_object.save()
    context={}
    context['total_price'] = grand_total
    return render(request,'order_placed.html',context)

def my_orders(request):
    if 'customer_login' in request.session:
        user_name=request.session['customer_login']
        
    user_object=Customer.objects.get(user_name=user_name)
    order_objects = Order.objects.filter(user_name=user_object)
        
    context={}
    context['my_orders'] = order_objects
    print(len(order_objects))
    for order in order_objects:
        for d in order.cart.all():
            print(d)

    return render(request,'my_orders.html',context)
   


def forgot_password(request):
    return render(request,'forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
            customer_email = request.POST['user_email']
        
            customer_object=Customer.objects.get(user_email=customer_email)
            MAX_LEN = 12
            DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                                'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                                'z']
            UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                                'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                'Z']
            SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                    '*', '(', ')', '<']
            COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
            rand_digit = random.choice(DIGITS)
            rand_upper = random.choice(UPCASE_CHARACTERS)
            rand_lower = random.choice(LOCASE_CHARACTERS)
            rand_symbol = random.choice(SYMBOLS)
            temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
            
            for x in range(MAX_LEN - 4):
                temp_pass = temp_pass + random.choice(COMBINED_LIST)

                
                temp_pass_list = array.array('u', temp_pass)
                random.shuffle(temp_pass_list)

            password = ""
            for x in temp_pass_list:
                    password = password + x
            subject = 'Reset Password'
            message = f'Hi {{customer_object.user_name}} Your new password is {{password}}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [customer_email, ]
            send_mail( subject, message, email_from, recipient_list )
            customer_object.user_password = password
            customer_object.save()
            messages.info(request,'Your new password is sent to your email')
            return redirect('login_page')

def delete_item_from_cart(request,cart_id):
    cart_object = Cart.objects.get(cart_id=cart_id)
    cart_object.delete()
    return redirect('cart_page')

def date_wise_analytics(request):
    return render(request,'chart.html')

def date_wise_analytics_results(request):
    date_wise_list=[]
    labels = []
    if request.method == 'POST':
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        if start_date == end_date:
            messages.info(request,'Start date and end date could not be the same')
            return redirect('date_wise_analytics_page')
        date_range=pd.date_range(start=start_date, end=end_date)
        for d in date_range:
            labels.append(d.date())
            dish_objects=Order.objects.filter(order_date=d.date()).count()
            if dish_objects:
                date_wise_list.append(dish_objects)
            
        return render(request, 'date_wise_analytics.html', {
        'labels': labels,
        'dataset': date_wise_list,
    })

def date_wise_orders(request):
    if 'customer_login' in request.session:
        user_name=request.session['customer_login']
        user_object = Customer.objects.get(user_name=user_name)
    context = {}
    order_objects = []
    if request.method == 'POST':
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        if start_date == '' or end_date == '':
            messages.error(request,'Dates cannot be empty')
            return redirect('my_orders')
        if start_date == end_date:
            messages.info(request,'Start date and end date could not be the same')
            return redirect('my_orders')
        date_range=pd.date_range(start=start_date, end=end_date)
        for d in date_range:
            order_object = Order.objects.filter(order_date=d.date(),user_name=user_object)
            if order_object:
                order_objects.append(order_object)
        messages.info(request,'Orders in selected date range are ')
        context['my_orders'] = order_objects
        return render(request,'date_wise_orders.html',context)

def search_for_order(request):
    context = {}
    if 'q' in request.GET:
        q = request.GET.get('q')
        if 'customer_login' in request.session:
            user_name = request.session['customer_login']
        user_object = Customer.objects.get(user_name=user_name)
        
        searching_order_objects = Order.objects.get(order_id__icontains=q,user_name=user_object)
        context['searching_order_object'] = searching_order_objects
    return render(request,'my_orders.html',context)

def edit_restaurant_details(request):
    if 'restaurant_login' in request.session:
        user_name = request.session['restaurant_login']
        user_object = Customer.objects.get(user_name=user_name)
        return render(request,'add_restaurant_details.html',{'user_name':user_name})
    else:
        return redirect('login_page')


    

    
        





  
    
    






    
