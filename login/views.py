from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Notification
from recipe.models import Recipe

# Create your views here.
        
def index(request):
    return HttpResponseRedirect('login/')

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('../../recipes/home/')
    notifications = Notification.objects.filter(to_user=request.user.username)
    if request.method == 'POST':
        if login_authenticate(request):
            return HttpResponseRedirect('../../recipes/home/')
        else:
            username = request.POST.get('email')
            content = {'incorrect': 'Email or Password is Incorrect', 'email_input': username, 'notifications': notifications}
            return render(request, 'login/login.html', content)
    content = {'notifications': notifications}
    return render(request, 'login/login.html', content)

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
    if request.user.is_authenticated:
        return HttpResponseRedirect('../../recipes/home/')
    notifications = Notification.objects.filter(to_user=request.user.username)
    if request.method == 'POST':
        if sign_up_create(request):
            return HttpResponseRedirect('/')
        else:
            content = {'incorrect': 'An Account Already Has That Email', 'notifications': notifications}
            return render(request, 'login/sign_up.html', content)
    content = {'notifications': notifications}
    return render(request, 'login/sign_up.html', content)

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

def notifications(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../get-started/login/')
    notifications_details = Notification.objects.filter(to_user=request.user.username)
    notifications = list()
    from_users = list()
    for item in notifications_details:
        notifications.append(Recipe.objects.get(encrypt=item.recipe_id))
    for item in notifications_details:
        from_users.append(item.from_user)
    content = {'notifications': notifications, 'users': from_users}
    return render(request, 'login/notifications.html', content)

def accept_invitation(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    notification = get_object_or_404(Notification, to_user=request.user.username, recipe_id=enc)
    recipe.users.append(request.user.username)
    recipe.save()
    notification.delete()
    return HttpResponseRedirect("../../")

def decline_invitation(request, enc):
    notification = get_object_or_404(Notification, to_user=request.user.username, recipe_id=enc)
    notification.delete()
    return HttpResponseRedirect("../../")

def settings(request):
    return HttpResponseRedirect('')