from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_snum = models.CharField(max_length=50)
    room_name = models.CharField(max_length=50)
    room_pin = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.room_name

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
        return self.cust_firstname

# Form models
class RoomLoginForm(forms.Form):
    room_snum = forms.CharField(label='Room Serial Number', max_length=50)
    room_pin = forms.CharField(label='Pin Code', max_length=50)

class CheckinForm(forms.Form):
    cust_firstname = forms.CharField(label='First Name', max_length=50)
    cust_lastname = forms.CharField(label='Last Name', max_length=50)
    cust_phonenumber = forms.CharField(label='Phone Number', max_length=50)
    cust_country = forms.CharField(label='Country', max_length=50)
    cust_state = forms.CharField(label='State', max_length=50)
    cust_city = forms.CharField(label='City', max_length=50)
    cust_address = forms.CharField(label='Address', max_length=200)
    cust_passport_number = forms.CharField(label='Passport Number', max_length=100)
    cust_checkin_date = forms.DateTimeField(label='Checkin Date')
    cust_checkout_date = forms.DateTimeField(label='Checkout Date')
    cust_id_image = forms.ImageField(label='Picture of Id')