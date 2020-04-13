
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
]
