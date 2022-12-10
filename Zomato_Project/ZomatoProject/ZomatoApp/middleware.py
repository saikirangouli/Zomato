from django.shortcuts import render,redirect
from .urls import *

def auth_middleware(get_response):
    def Admin(request):
        context={}
        if 'customer_login' in request.session:
            user_name=request.session['customer_login']
            context['user_name'] = user_name  

            return redirect(logindetails)
   
        response = get_response(request)

        return response
    return Admin