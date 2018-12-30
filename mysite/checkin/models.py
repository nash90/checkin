from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.CharField(max_length=50)
    room_name = models.CharField(max_length=50)
    room_pin = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    cust_firstname = models.CharField(max_length=50)
    cust_lastname = models.CharField(max_length=50)
    cust_phonenumber = models.CharField(max_length=50)
    cust_country = models.CharField(max_length=50)
    cust_state = models.CharField(max_length=50)
    cust_city = models.CharField(max_length=50)
    cust_address = models.CharField(max_length=200)
    cust_passport_number = models.CharField(max_length=100)
    cust_checkin_date = models.DateTimeField('checkin')
    cust_checkout_date = models.DateTimeField('checkout')

    def __str__(self):
        return self.name
