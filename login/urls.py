
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('login-authenticate/', views.login_authenticate, name='login_authenticate'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-up-create/', views.sign_up_create, name='sign_up_create'),
]
