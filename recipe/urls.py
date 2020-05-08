
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('appetizers/', views.appetizers, name='appetizers'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('dinner/', views.dinner, name='dinner'),
    path('desserts/', views.desserts, name='desserts'),
    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('create-recipe/create/', views.create, name='create'),
    path('view-recipe/<uuid:enc>/', views.view_recipe, name='view_recipe'),
    path('edit-recipe/<uuid:enc>/', views.edit_recipe, name='edit_recipe'),
    path('edit-recipe/<uuid:enc>/edit/', views.edit, name='edit'),
    path('edit-people/<uuid:enc>/', views.edit_people, name='edit_people'),
    path('edit-people/<uuid:enc>/people/', views.people, name='people'),
    path('delete-recipe/<uuid:enc>/', views.delete_recipe, name='delete_recipe'),
    path('remove-recipe/<uuid:enc>/', views.remove_recipe, name='remove_recipe'),
]