from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("logout/", views.logout_view, name="logout"),
    path("notifications/", views.notifications, name="notifications"),
    path(
        "notifications/accept/<uuid:enc>/",
        views.accept_invitation,
        name="accept_invitation",
    ),
    path(
        "notifications/decline/<uuid:enc>/",
        views.decline_invitation,
        name="decline_invitation",
    ),
    path("settings/", views.settings, name="settings"),
    path("settings/edit", views.settings_edit, name="settings_edit"),
    re_path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate,
        name="activate",
    ),
    path("account-activated/", views.activate_success, name="activate_success"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.reset,
        name="reset",
    ),
    path("reset-password/", views.reset_password, name="reset_password"),
    re_path(
        r"^settings/change-password/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.change_password,
        name="change_password",
    ),
    path("settings/password-changed/", views.password_changed, name="password_changed"),
    path(
        "verification-email-sent/",
        views.verification_email_sent,
        name="verification_email_sent",
    ),
]
