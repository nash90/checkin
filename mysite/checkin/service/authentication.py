from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

class Signup:
    def __init__(self):
        pass
    
    def create_user(self, form):
        form.save()
    
    def create_form(self):
        return UserCreationForm()
    
    def login_user(self, form, request):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
        login(request, user)




