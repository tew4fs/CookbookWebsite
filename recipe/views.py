from django.db import models
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from login.models import Notification, Unverified
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from .models import Recipe

from typing import Any, Dict, Optional


# Create your views here.
@login_required
def index(request):
    return HttpResponseRedirect("home/")


@method_decorator(login_required, name="dispatch")
class AllRecipes(TemplateView):
    template_name = "recipe/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = Recipe.objects.filter(pk__contains=self.request.user.pk)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        query = self.request.GET.get("q")
        if query:
            recipes = search(query, recipes)
        context["recipes"] = recipes
        context["notifications"] = notifications
        return context


@method_decorator(login_required, name="dispatch")
class Appetizers(TemplateView):
    template_name = "recipe/appetizers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appetizers_recipes = Recipe.objects.filter(recipe_type="Appetizers", pk__contains=self.request.user.pk)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        query = self.request.GET.get("q")
        if query:
            appetizers_recipes = search(query, appetizers_recipes)
        context["appetizers"] = appetizers_recipes
        context["notifications"] = notifications
        return context


@method_decorator(login_required, name="dispatch")
class Breakfast(TemplateView):
    template_name = "recipe/breakfast.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breakfast_recipes = Recipe.objects.filter(recipe_type="Breakfast", pk__contains=self.request.user.pk)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        query = self.request.GET.get("q")
        if query:
            breakfast_recipes = search(query, breakfast_recipes)
        context["breakfast"] = breakfast_recipes
        context["notifications"] = notifications
        return context


@method_decorator(login_required, name="dispatch")
class Dinner(TemplateView):
    template_name = "recipe/dinner.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dinner_recipes = Recipe.objects.filter(recipe_type="Dinner", pk__contains=self.request.user.pk)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        query = self.request.GET.get("q")
        if query:
            dinner_recipes = search(query, dinner_recipes)
        context["dinner"] = dinner_recipes
        context["notifications"] = notifications
        return context


@method_decorator(login_required, name="dispatch")
class Desserts(TemplateView):
    template_name = "recipe/desserts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        desserts_recipes = Recipe.objects.filter(recipe_type="Dessert", pk__contains=self.request.user.pk)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        query = self.request.GET.get("q")
        if query:
            desserts_recipes = search(query, desserts_recipes)
        context["desserts"] = desserts_recipes
        context["notifications"] = notifications
        return context


@method_decorator(login_required, name="dispatch")
class CreateRecipe(CreateView):
    model = Recipe
    template_name = "recipe/create-recipe.html"
    fields = ["recipe_name", "recipe_type", "description", "cook_time", "serves", "ingredients", "steps"]
    success_url = "."

    def form_valid(self, form):
        is_valid = super().form_valid(form)
        self.object.owner = self.request.user.pk
        self.object.save()
        return is_valid


@method_decorator(login_required, name="dispatch")
class ViewRecipe(DetailView):
    model = Recipe
    template_name = "recipe/view-recipe.html"
    context_object_name = "recipe"

    def get_object(self, queryset=None):
        return Recipe.objects.get(uid=self.kwargs.get("uid"))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_owner"] = context["recipe"].owner == self.request.user.pk
        context["notifications"] = Notification.objects.filter(to_user=self.request.user.pk)
        return context


@method_decorator(login_required, name="dispatch")
class EditRecipe(UpdateView):
    model = Recipe
    template_name = "recipe/edit-recipe.html"
    fields = ["recipe_name", "recipe_type", "description", "cook_time", "serves", "ingredients", "steps"]

    def get_object(self, queryset=None):
        return Recipe.objects.get(uid=self.kwargs.get("uid"))


@method_decorator(login_required, name="dispatch")
class EditPeople(UpdateView):
    model = Recipe
    template_name = "recipe/edit-people.html"
    fields = ["users"]

    def get_object(self, queryset=None):
        return Recipe.objects.get(uid=self.kwargs.get("uid"))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["owner_email"] = self.request.user.username
        return context

    def form_valid(self, form):
        is_valid = super().form_valid(form)
        print(self.object.users)
        return is_valid


@login_required
def delete_recipe(request, uid):
    recipe = get_object_or_404(Recipe, uid=uid)
    if request.user.pk != recipe.owner:
        return HttpResponseRedirect("../../view-recipe/" + str(recipe.encrypt) + "/")
    recipe.delete()
    return HttpResponseRedirect("../../")


@login_required
def remove_recipe(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    user_list = list()
    for item in recipe.users:
        if item != request.user.pk:
            user_list.append(item)
    recipe.users.clear()
    for item in user_list:
        recipe.users.append(item)
    recipe.save()
    return HttpResponseRedirect("../../")


def search(query, recipes):
    recipes = recipes.filter(recipe_name__icontains=query)
    recipes_query_descriptions = recipes.filter(description__contains=query)
    return (recipes | recipes_query_descriptions).distinct()
