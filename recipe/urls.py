from django.urls import path
from . import views
from recipe.views import (
    AllRecipes,
    Appetizers,
    Breakfast,
    Dinner,
    Desserts,
    CreateRecipe,
    EditRecipe,
    EditPeople,
    ViewRecipe,
)

app_name = "recipe"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", AllRecipes.as_view(), name="home"),
    path("appetizers/", Appetizers.as_view(), name="appetizers"),
    path("breakfast/", Breakfast.as_view(), name="breakfast"),
    path("dinner/", Dinner.as_view(), name="dinner"),
    path("desserts/", Desserts.as_view(), name="desserts"),
    path("create-recipe/", CreateRecipe.as_view(), name="create_recipe"),
    path("view-recipe/<uuid:uid>/", ViewRecipe.as_view(), name="view_recipe"),
    path("edit-recipe/<uuid:uid>/", EditRecipe.as_view(), name="edit_recipe"),
    path("edit-people/<uuid:uid>/", EditPeople.as_view(), name="edit_people"),
    path("delete-recipe/<uuid:uid>/", views.delete_recipe, name="delete_recipe"),
    path("remove-recipe/<uuid:uid>/", views.remove_recipe, name="remove_recipe"),
]
