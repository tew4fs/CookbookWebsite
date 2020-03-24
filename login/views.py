from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User



# Create your views here.

        
def index(request):
    return HttpResponseRedirect('login/')

def login_view(request):
    return render(request, 'login/login.html')

def login_authenticate(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    print(username)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('../login/')

def sign_up(request):
    return render(request, 'login/sign_up.html')

def sign_up_create(request):
    email = request.POST.get('email_1')
    password = request.POST.get('password_1')
    first_name_form = request.POST.get('first_name')
    last_name_form = request.POST.get('last_name')
    user = User.objects.create_user(email, email, password)
    user.first_name = first_name_form
    user.last_name = last_name_form
    user.save()
    return HttpResponseRedirect('/')