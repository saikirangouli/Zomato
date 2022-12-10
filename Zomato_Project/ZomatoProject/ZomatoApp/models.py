
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True, editable=False) 
    full_name = models.CharField(max_length=40)
    user_name = models.CharField(max_length=30)
    user_email = models.EmailField()
    user_password = models.CharField(max_length=30)
    user_type = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer_id) +' '+str(self.user_name)+' '+str(self.user_type)

        
class User_session(models.Model):
    user_session_id = models.OneToOneField(Customer,on_delete=models.CASCADE)


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True,editable=False)
    restaurant_name = models.CharField(max_length=20)
    restaurant_adress = models.TextField()
    restaurant_owner_name = models.OneToOneField(Customer,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.restaurant_name)

class Dish(models.Model):
    dish_id = models.AutoField(primary_key=True,editable=False)
    dish_name = models.CharField(max_length=40)
    dish_price = models.IntegerField()
    dish_image = models.ImageField(upload_to="Item_images")
    restaurant_name = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dish_name)+' '+' '+str(self.restaurant_name)


class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True,editable=False)
    user_name=models.ForeignKey(Customer,on_delete=models.CASCADE)
    dishes=models.ForeignKey(Dish,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField(default=0)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return str(self.dishes)




class Order(models.Model):
    order_id=models.AutoField(primary_key=True,editable=False)
    user_name= models.ForeignKey(Customer,on_delete=models.CASCADE)
    cart=models.ManyToManyField('Cart',related_name='cart',related_query_name='cart_objects')
    order_date=models.DateField()
    total_price=models.IntegerField()

    def __str__(self):
        return str(self.cart)



       
