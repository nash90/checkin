from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.core import serializers
from django import forms
from django.core.mail import EmailMessage
import jwt
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from .models import RoomLoginForm
from .models import CheckinForm
from .models import Room
from .models import Customer
from .service.authentication import Signup
from .service.checkin import RoomService
from .service.checkin import CustomerService

# Create your views here.

from django.http import HttpResponse

secret_key = 'thisneedstochange'

def home(request):
    token_info = getRoomToken(request)

    if validObject(token_info):
        context = {
          'form': CheckinForm()
        }
        return render(request, 'customer-form.html', context)
    else:
        context = {
          'form': RoomLoginForm()
        }
        return render(request, 'home.html', context)

def signup(request):
    signup = Signup()
    if request.method == 'POST':        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            signup.create_user(form)
            signup.login_user(form, request)
            return redirect('home')
    else:
        form = signup.create_form()

    context = {
        "form":form
    }
    return render(request, 'signup.html', context)

def room_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RoomLoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = dict(form.cleaned_data)
            room_snum = data['room_snum']
            room_pin = data['room_pin']
            #print("snum",room_snum)
            room = RoomService().getByRoomSnum(room_snum)[0]

            if(room != None and checkValidRoomPin(room, room_pin)):
                room = {
                  "room_snum":room.room_snum,
                  "room_pin":room.room_pin
                }
                token = getJWTToken(room)
                response = redirect('home')
                response.set_cookie(key='ROOM_TOKEN', value=token)
                #print("room login success")
                return response
        form.add_error(None,"Room Login Fail")
        context = {
          "form":form
        }
        #print("room login Fail")
        return render(request, 'home.html',context)
    else:
        raise Http404("Not Found")


def room_logout(request):
    response = redirect('home')
    response.delete_cookie(key='ROOM_TOKEN')
    return response

def room_customer(request):
    if request.method == 'POST':
        token_info = getRoomToken(request)    
        if validObject(token_info):
            form = CheckinForm(request.POST, request.FILES)
            files = request.FILES
            if form.is_valid():
                save_customer(form.cleaned_data, token_info['room_snum'])
                send_client_email(form, token_info['room_snum'], files["cust_id_image"])
                return redirect('home')
            else:
                context = {
                    'form':form
                }
                return render(request, 'customer-form.html', context)
        return redirect('room_logout')
    raise Http404("Not Found")

## Helper Functions

def validObject(obj):
    flag = False
    if(obj != None):
      flag = True
    return flag

def checkValidRoomPin(room, room_pin):
    if(room.room_pin == room_pin):
        return True
    else:
        return False

def getJWTToken(data):
    encoded_token = jwt.encode(data, secret_key, algorithm='HS256')
    return encoded_token.decode('UTF-8')

def decryptJWTToken(token):
    #print("token:",str(token))
    data = {}
    try:
      data = jwt.decode(token, secret_key, algorithms=['HS256'])
    except Exception as e:
      raise Http404("Invalid Token")
    return data

def getRoomToken(request):
    room_token = request.COOKIES.get('ROOM_TOKEN')
    token_info = None
    if(validObject(room_token)):      
      token_info = decryptJWTToken(room_token)
    return token_info

def save_customer(form, room_snum):
    room = RoomService().getByRoomSnum(room_snum)[0]
    #print(form)
    customer = Customer(
        room = room,
        cust_firstname = form["cust_firstname"],
        cust_lastname = form["cust_lastname"],
        cust_phonenumber = form["cust_phonenumber"],
        cust_country = form["cust_country"],
        cust_state = form["cust_state"],
        cust_city = form["cust_city"],
        cust_address = form["cust_address"],
        cust_passport_number = form["cust_passport_number"],
        cust_checkin_date = form["cust_checkin_date"],
        cust_checkout_date = form["cust_checkout_date"],
    )
    #print(customer.__dict__)
    CustomerService().saveCustomer(customer)

def send_email(param):
    #print(param)
    subject = param["subject"]
    body = param["body"]
    from_address = param["from_address"]
    to_address = param["to_address"]
    attachments = param["attachments"]
    header = {
        "content-type":"text/html"
    }
    if subject and body and from_address and to_address:        
        email = EmailMessage(subject=subject, body=body, from_email=from_address, to=to_address)
        if validObject(attachments):
            images= []
            image = MIMEImage(attachments.read())
            image.add_header('Content-Disposition', 'attachment', filename="Id Picture")
            images.append(image)
            email.attachments=images
        try:
            email.send()
        except Exception as e:
            print("Error: ",e)
            raise Http404("Failed to Send Email")


def send_client_email(form, room_snum, files):
    #print(form)
    data = form.cleaned_data
    data["room_snum"] = room_snum
    user = RoomService().getUserByRoomSnum(room_snum)
    print(dir(user))
    user_email = user.email
    print(user_email)
    subject = room_snum + ": Customer Information"
    body = generateBody(checkin_mail_template, data)
    from_address = "support@yamacity.com"
    to_address = [user_email]
    attachments=files
    param = {
        "subject":subject,
        "body":body,
        "from_address":from_address,
        "to_address":to_address,
        "attachments":attachments
    }
    #print(body)
    send_email(param)

def generateBody(template, data):
    #print(data)
    del data["cust_id_image"]
    for key in data.keys():
        replace_key = "{{" + key + "}}"
        if(validObject(key)):
            value = data.get(key)
            if (isinstance(value, datetime.datetime)):
                value = value.strftime("%Y-%m-%d")           
            template = template.replace(replace_key,getLabelAndValue(key, value))
        template = template.replace(replace_key, "Not provided")
    return template

def getLabelAndValue(key, value):
    if(key == "room_snum"):
        return "Room Serial Number: "+value
    if(key == "cust_firstname"):
        return "First Name: "+value
    if(key == "cust_lastname"):
        return "Last Name: "+value
    if(key == "cust_phonenumber"):
        return "Phone Number: "+value
    if(key == "cust_country"):
        return "Country: "+value
    if(key == "cust_state"):
        return "State: "+value
    if(key == "cust_city"):
        return "City: "+value
    if(key == "cust_address"):
        return "Address: "+value
    if(key == "cust_passport_number"):
        return "Passport: "+value
    if(key == "cust_checkin_date"):
        return "Chekin Date: "+value
    if(key == "cust_checkout_date"):
        return "Checkout Date: "+value

checkin_mail_template = '''
Dear User,

Checkin information has been received.
{{room_snum}}
{{cust_firstname}}
{{cust_lastname}}
{{cust_phonenumber}}
{{cust_country}}
{{cust_state}}
{{cust_city}}
{{cust_address}}
{{cust_passport_number}}
{{cust_checkin_date}}
{{cust_checkout_date}}

With Regards,

'''