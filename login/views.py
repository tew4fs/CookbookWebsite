from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from Cookbook.settings import EMAIL_HOST_USER
from .models import Notification, Unverified
from .tokens import account_activation_token
from recipe.models import Recipe

# Create your views here.


def index(request):
    return HttpResponseRedirect("login/")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("recipe:home")
    notifications = Notification.objects.filter(to_user=request.user.pk)
    if request.method == "POST":
        if login_authenticate(request):
            return redirect("login")
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


def forgot_password(request):
    if request.method == "POST":
        user_valid = User.objects.filter(username=request.POST.get("email"))
        if user_valid:
            user = User.objects.get(username=request.POST.get("email"))
            current_site = get_current_site(request)
            subject = "Reset Password"
            message = render_to_string(
                "login/reset-password-email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [
                    request.POST.get("email"),
                ],
                fail_silently=True,
            )
        return render(request, "login/recovery-email-sent.html")
    return render(request, "login/forgot-password.html")


def reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        content = {"email": user.username}
        return render(request, "login/reset-password.html", content)
    else:
        return HttpResponseRedirect("/")


def reset_password(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST.get("email"))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            password = request.POST.get("password_1")
            user.set_password(password)
            user.save()
        return redirect("login")
    else:
        return HttpResponseRedirect("/")


def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("../../recipes/home/")
    notifications = Notification.objects.filter(to_user=request.user.pk)
    if request.method == "POST":
        if sign_up_create(request):
            email = request.POST.get("email_1")
            send_verification_email(request, email)
            return redirect("verification_email_sent")
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
        # unverified = Unverified(user=email)
        # unverified.save()
        user = authenticate(username=email, password=password)
        login(request, user)
        return True
    else:
        return False


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        unverified = Unverified.objects.get(user=user.username)
        unverified.delete()
        return redirect("activate_success")
    else:
        return redirect("home")


def activate_success(request):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    content = {"notifications": notifications}
    return render(request, "login/activate-success.html", content)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def notifications(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("../../get-started/login/")
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
    return HttpResponseRedirect("../../")


def decline_invitation(request, enc):
    notification = get_object_or_404(Notification, to_user=request.user.pk, recipe_id=enc)
    notification.delete()
    return HttpResponseRedirect("../../")


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
                send_verification_email(request, username)
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


def send_verification_email(request, email):
    current_site = get_current_site(request)
    subject = "Verify Account"
    message = render_to_string(
        "login/acc-email-verification.html",
        {
            "user": request.user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
            "token": account_activation_token.make_token(request.user),
        },
    )
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [
            email,
        ],
        fail_silently=True,
    )


def verification_email_sent(request):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    content = {"notifications": notifications}
    return render(request, "login/verification-email-sent.html", content)
