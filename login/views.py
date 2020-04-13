from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User



# Create your views here.

        
def index(request):
    return HttpResponseRedirect('login/')

def login_view(request):
    if request.method == 'POST':
        if login_authenticate(request):
            return HttpResponseRedirect('/')
        else:
            username = request.POST.get('email')
            content = {'incorrect': 'Email or Password is Incorrect', 'email_input': username}
            return render(request, 'login/login.html', content)
    return render(request, 'login/login.html')

def login_authenticate(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    else:
        return False

def sign_up(request):
    if request.method == 'POST':
        if sign_up_create(request):
            return HttpResponseRedirect('/')
        else:
            content = {'incorrect': 'An Account Already Has That Email'}
            return render(request, 'login/sign_up.html', content)
    return render(request, 'login/sign_up.html')

def sign_up_create(request):
    email = request.POST.get('email_1')
    user_emails = User.objects.filter(username=email)
    if user_emails.count() is 0:
        password = request.POST.get('password_1')
        first_name_form = request.POST.get('first_name')
        last_name_form = request.POST.get('last_name')
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name_form
        user.last_name = last_name_form
        user.save()
        user = authenticate(username=email, password=password)
        login(request, user)
        return True
    else:
       return False

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')