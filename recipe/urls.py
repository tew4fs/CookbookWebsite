
from django.urls import path
from . import views
from recipe.views import Appetizers, Breakfast

app_name = "recipe"

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('appetizers/', Appetizers.as_view(), name='appetizers'),
    path('breakfast/', Breakfast.as_view(), name='breakfast'),
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
    path('remove-picture/<uuid:enc>/', views.remove_picture, name="remove_picture"),
]