
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/accept/<uuid:enc>/', views.accept_invitation, name='accept_invitation'),
    path('notifications/decline/<uuid:enc>/', views.decline_invitation, name='decline_invitation'),
    path('settings/', views.settings, name='settings'),
]
