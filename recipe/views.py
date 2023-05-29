from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.utils.decorators import method_decorator

from recipe.models import Recipe
from login.models import Notification

from typing import Any, Dict


# Create your views here.
@login_required
def index(request):
    return redirect("recipe:home")


@method_decorator(login_required, name="dispatch")
class AllRecipes(TemplateView):
    template_name = "recipe/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = Recipe.objects.filter(owner=self.request.user.pk)
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
        user = self.request.user
        query = self.request.GET.get("q")
        context["appetizers"] = _get_recipes("Appetizer", user.pk, user.username, query)
        context["notifications"] = _get_notifications(self.request.user.pk)
        return context


@method_decorator(login_required, name="dispatch")
class Breakfast(TemplateView):
    template_name = "recipe/breakfast.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        query = self.request.GET.get("q")
        context["breakfast"] = _get_recipes("Breakfast", user.pk, user.username, query)
        context["notifications"] = _get_notifications(self.request.user.pk)
        return context


@method_decorator(login_required, name="dispatch")
class Dinner(TemplateView):
    template_name = "recipe/dinner.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        query = self.request.GET.get("q")
        context["dinner"] = _get_recipes("Dinner", user.pk, user.username, query)
        context["notifications"] = _get_notifications(self.request.user.pk)
        return context


@method_decorator(login_required, name="dispatch")
class Desserts(TemplateView):
    template_name = "recipe/desserts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        query = self.request.GET.get("q")
        context["desserts"] = _get_recipes("Dessert", user.pk, user.username, query)
        context["notifications"] = _get_notifications(self.request.user.pk)
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
        return redirect("recipe:view_recipe", kwargs={"uid": recipe.uid})
    recipe.delete()
    return redirect("recipe:home")


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
    return redirect("recipe:home")


def search(query, recipes):
    recipes = recipes.filter(recipe_name__icontains=query)
    recipes_query_descriptions = recipes.filter(description__contains=query)
    return (recipes | recipes_query_descriptions).distinct()


def _get_recipes(recipe_type: str, user_pk:int, username: str, query: str):
    recipes = Recipe.objects.filter(recipe_type=recipe_type, owner=user_pk)
    if query:
        recipes = search(query, recipes)
    return recipes


def _get_notifications(pk: int):
    return Notification.objects.filter(to_user=pk)
