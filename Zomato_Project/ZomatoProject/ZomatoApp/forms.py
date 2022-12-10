from django.forms import ModelForm
from .models import *

class SignupForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'