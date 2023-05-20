from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from login.models import Notification, Unverified
from login.tokens import account_activation_token
from recipe.models import Recipe


def index(request):
    return redirect("login:login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("recipe:home")
    notifications = Notification.objects.filter(to_user=request.user.pk)
    if request.method == "POST":
        if login_authenticate(request):
            return redirect("login:login")
        else:
            username = request.POST.get("email")
            content = {
                "incorrect": "Email or Password is Incorrect",
                "email_input": username,
                "notifications": notifications,
            }
            return render(request, "login/login.html", content)
    content = {"notifications": notifications}
    return render(request, "login/login.html", content)


def login_authenticate(request):
    username = request.POST.get("email")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    else:
        return False


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("recipe:home")
    notifications = Notification.objects.filter(to_user=request.user.pk)
    if request.method == "POST":
        if sign_up_create(request):
            return redirect("login:login")
        else:
            content = {
                "incorrect": "An Account Already Has That Email",
                "notifications": notifications,
            }
            return render(request, "login/sign_up.html", content)
    content = {"notifications": notifications}
    return render(request, "login/sign_up.html", content)


def sign_up_create(request):
    email = request.POST.get("email_1")
    user_emails = User.objects.filter(username=email)
    if user_emails.count() == 0:
        password = request.POST.get("password_1")
        first_name_form = request.POST.get("first_name")
        last_name_form = request.POST.get("last_name")
        user = User.objects.create_user(username=email, email=email, password=password)
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
    return redirect("landing:index")


def notifications(request):
    if request.user.is_authenticated is False:
        return redirect("login:login")
    notifications_details = Notification.objects.filter(to_user=request.user.pk)
    notifications = list()
    from_users = list()
    for item in notifications_details:
        notifications.append(Recipe.objects.get(encrypt=item.recipe_id))
    for item in notifications_details:
        from_users.append(User.objects.get(pk=item.from_user))
    content = {
        "notifications": notifications_details,
        "notification_list": notifications,
        "from_users": from_users,
    }
    return render(request, "login/notifications.html", content)


def accept_invitation(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    notification = get_object_or_404(Notification, to_user=request.user.pk, recipe_id=enc)
    recipe.users.append(request.user.pk)
    recipe.save()
    notification.delete()
    return redirect("login:notifications")


def decline_invitation(request, enc):
    notification = get_object_or_404(Notification, to_user=request.user.pk, recipe_id=enc)
    notification.delete()
    return redirect("login:notifications")


def settings(request):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    valid_username = True
    change_username = False
    if request.method == "POST":
        if request.POST.get("current_password") is not None:
            if request.user.check_password(request.POST.get("current_password")):
                token = account_activation_token.make_token(request.user)
                return redirect("change_password", token=token)
            else:
                content = {"incorrect": "The Password Entered Did Not Match Your Password"}
                return render(request, "login/settings.html", content)
        username = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user = request.user
        if user.username != username:
            user_emails = User.objects.filter(username=username)
            if user_emails.count() == 0:
                delete_from_DB = Unverified.objects.filter(user=user.username)
                for item in delete_from_DB:
                    item.delete()
                user.username = username
                unverified = Unverified(user=username)
                unverified.save()
                user.email = username
                change_username = True
            else:
                valid_username = False
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    if valid_username and change_username:
        return redirect("verification_email_sent")
    if valid_username:
        content = {"notifications": notifications}
        return render(request, "login/settings.html", content)
    else:
        content = {
            "notifications": notifications,
            "incorrect": "An Account Already Has That Email",
        }
        return render(request, "login/settings.html", content)


def settings_edit(request):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    content = {"notifications": notifications}
    return render(request, "login/settings-edit.html", content)


def change_password(request, token):
    if account_activation_token.check_token(request.user, token):
        notifications = Notification.objects.filter(to_user=request.user.pk)
        content = {"token": token, "notifications": notifications}
        return render(request, "login/change-password.html", content)
    else:
        redirect("settings")


def password_changed(request):
    if request.method == "POST":
        user = request.user
        password = request.POST.get("password_1")
        user.set_password(password)
        user.save()
        user = authenticate(username=user.username, password=password)
        login(request, user)
    return redirect("settings")
