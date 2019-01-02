from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import F
from django.db.models import Count
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ..models import Room
from ..models import Customer


class RoomService():
    def __init__(self):
        pass

    def getAll(self):
        rooms = None
        try:
            rooms = Room.objects.all()
        except Exception as e: 
          raise Http404("DB Error: Cant get all rooms")
        return rooms
    
    def getById(self, id):
        rooms = None
        try:
            rooms = Room.objects.get(id=id)
        except Exception as e: 
          raise Http404("DB Error: Cant get room by id")
        return rooms

    def getByRoomSnum(self, id):
        rooms = None
        try:
            rooms = Room.objects.filter(room_snum = id)
        except Exception as e: 
          raise Http404("DB Error: Cant get room by sequence number")
        return rooms

    def getUserByRoomSnum(self, room_snum):
        user = None
        try:
            room = Room.objects.filter(room_snum = room_snum)
            #print(room)
            user = room[0].user
        except Exception as e:
            print(e) 
            raise Http404("DB Error: Cant get User by room snum")
        return user

class CustomerService():
    def __init__(self):
        pass

    def getAll(self):
        customers = None
        try:
            customers = Customer.objects.all()
        except Exception as e: 
            raise Http404("DB Error: Cant get all customers")
        return customers
    
    def saveCustomer(self, customer):
        try:
            #print(customer)
            customer.save()            
        except Exception as e: 
            print(e)
            raise Http404("DB Error: Cant save customer")