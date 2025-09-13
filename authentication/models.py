from django.db import migrations,models
import django.db.models.deletion
from django.conf import settings
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,User
from django.utils.translation import gettext_lazy as _
import datetime
import pytz
#from authentication.models import FoodItem


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# accounts/models.py


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email



class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='food_items', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

IST = pytz.timezone('Asia/Kolkata')

def get_ist_datetime():
    return datetime.datetime.now(IST)

# from django.db import models
# from django.conf import settings
# from .utils import get_ist_datetime  # Ensure this exists and is imported
# # from datetime import datetime (if needed for default)

# class Restaurant(models.Model):
#     name = models.CharField(max_length=100)
#     upi_id = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.name

# from django.db import models
# from django.conf import settings
# from .utils import get_ist_datetime
# class Order(models.Model):
#     PAYMENT_CHOICES = [
#         ('COD', 'Cash on Delivery'),
#         ('UPI', 'UPI Payment'),
#     ]

#     created_at = models.DateTimeField(auto_now_add=True)
#     date = models.DateTimeField(default=get_ist_datetime)

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
#     total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

#     is_ordered = models.BooleanField(default=False)
#     payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Order {self.pk} by {self.user.username}"

#     def placeOrder(self):
#         self.save()

#     @staticmethod
#     def get_orders_by_customer(customer_id):
#         return Order.objects.filter(user__id=customer_id).order_by('-date')

# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username



class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    is_ordered = models.BooleanField(default=False) 
    # date = models.DateField(default=datetime.datetime.today)
    date = models.DateTimeField(default=get_ist_datetime)
    
    def __str__(self):
        return f"Order {self.pk} by {self.user.username}"

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitem', on_delete=models.CASCADE)
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in order {self.order.id}"

