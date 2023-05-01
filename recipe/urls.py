from django.urls import path
from . import views
from recipe.views import Appetizers, Breakfast, CreateRecipe, ViewRecipe

app_name = "recipe"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("appetizers/", Appetizers.as_view(), name="appetizers"),
    path("breakfast/", Breakfast.as_view(), name="breakfast"),
    path("dinner/", views.dinner, name="dinner"),
    path("desserts/", views.desserts, name="desserts"),
    path("create-recipe/", CreateRecipe.as_view(), name="create_recipe"),
    path("view-recipe/<uuid:uid>/", ViewRecipe.as_view(), name="view_recipe"),
    path("edit-recipe/<uuid:uid>/", views.edit_recipe, name="edit_recipe"),
    path("edit-recipe/<uuid:uid>/edit/", views.edit, name="edit"),
    path("edit-people/<uuid:uid>/", views.edit_people, name="edit_people"),
    path("edit-people/<uuid:uid>/people/", views.people, name="people"),
    path("delete-recipe/<uuid:uid>/", views.delete_recipe, name="delete_recipe"),
    path("remove-recipe/<uuid:uid>/", views.remove_recipe, name="remove_recipe"),
    path("remove-picture/<uuid:uid>/", views.remove_picture, name="remove_picture"),
]
