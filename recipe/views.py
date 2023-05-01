from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth.models import User
from login.models import Notification, Unverified
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, DetailView
from .models import Recipe

from typing import Any, Dict


# Create your views here.
@login_required
def index(request):
    return HttpResponseRedirect("home/")


@login_required
def home(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("../../get-started/login/")
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "All", request)
        content = {"recipes": recipes}
    else:
        recipes = Recipe.objects.all().order_by("recipe_name")
        for rec in recipes:
            if request.user.pk not in rec.users:
                recipes = recipes.exclude(pk=rec.pk)
        content = {"notifications": notifications, "recipes": recipes}
    return render(request, "recipe/home.html", content)


@method_decorator(login_required, name="dispatch")
class Appetizers(TemplateView):
    template_name = "recipe/appetizers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        appetizers = Recipe.objects.filter(recipe_type="Appetizer")
        for recipe in appetizers:
            if self.request.user.pk not in recipe.users:
                appetizers = appetizers.exclude(pk=recipe.pk)
        context["appetizers"] = appetizers
        context["notifications"] = notifications
        return context


@method_decorator(login_required, name="dispatch")
class Breakfast(TemplateView):
    template_name = "recipe/breakfast.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        query = self.request.GET.get("q")
        if query:
            recipes = search(query, "Breakfast", self.request)
            context["recipes"] = recipes
        else:
            breakfast = Recipe.objects.filter(food_type="Breakfast")
            for rec in breakfast:
                if self.request.user.pk not in rec.users:
                    breakfast = breakfast.exclude(pk=rec.pk)
            context["breakfast"] = breakfast
            context["notifications"] = notifications
        return context

@login_required
def dinner(request):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "Dinner", request)
        content = {"recipes": recipes}
    else:
        dinner = Recipe.objects.filter(food_type="Dinner")
        for rec in dinner:
            if request.user.pk not in rec.users:
                dinner = dinner.exclude(pk=rec.pk)
        content = {"dinner": dinner, "notifications": notifications}
    return render(request, "recipe/dinner.html", content)


@login_required
def desserts(request):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "Dessert", request)
        content = {"recipes": recipes}
    else:
        desserts = Recipe.objects.filter(food_type="Dessert")
        for rec in desserts:
            if request.user.pk not in rec.users:
                desserts = desserts.exclude(pk=rec.pk)
        content = {"desserts": desserts, "notifications": notifications}
    return render(request, "recipe/dessert.html", content)


@method_decorator(login_required, name="dispatch")
class CreateRecipe(CreateView):
    model = Recipe
    template_name = "recipe/create-recipe.html"
    fields = ["recipe_name", "recipe_type", "description", "cook_time", "serves", "ingredients", "steps"]
    success_url = "."

    def form_valid(self, form):
        is_valid = super().form_valid(form)
        self.object.users.append(self.request.user.pk)
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
        context["is_owner"] = context["recipe"].users[0] == self.request.user.pk
        context["notifications"] = Notification.objects.filter(to_user=self.request.user.pk)
        return context


@login_required
def edit_recipe(request, enc):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return HttpResponseRedirect("../../view-recipe/" + str(recipe.encrypt) + "/")
    content = {"recipe": recipe, "notifications": notifications}
    return render(request, "recipe/edit-recipe.html", content)


@login_required
def edit(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return HttpResponseRedirect("../../../view-recipe/" + str(recipe.encrypt) + "/")
    recipe.food = request.POST.get("food")
    recipe.food_type = request.POST.get("foodCat")
    recipe.description = request.POST.get("description")
    recipe.steps.clear()
    recipe.ingredients.clear()
    for i in range(50):
        s = request.POST.get(str(i))
        if s is not None:
            recipe.steps.append(s)
    for i in range(100, 150):
        s = request.POST.get(str(i))
        if s is not None:
            recipe.ingredients.append(s)
    """
    if request.POST.get('pic') != "":
        pic = request.FILES['pic']
        pic_str = str(pic)
        pic_str = pic_str[len(pic_str)-4:len(pic_str)]
        if pic_str == '.png' or pic_str == '.jpg' or pic_str == 'jpeg' or pic_str == '.PNG' or pic_str == '.JPG' or pic_str == 'JPEG':
            fs = FileSystemStorage()
            pic_file = fs.save(pic.name, pic)
            url = fs.url(pic_file)
            recipe.picture = url
    """
    if request.POST.get("cook_time") is not None:
        recipe.cook_time = request.POST.get("cook_time")
    if request.POST.get("serves") is not None:
        recipe.serves = request.POST.get("serves")
    recipe.save()
    return HttpResponseRedirect("../../../view-recipe/" + str(recipe.encrypt) + "/")


@login_required
def remove_picture(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return redirect("home")
    recipe.picture = ""
    recipe.save()
    return redirect("edit_recipe", enc=enc)


@login_required
def edit_people(request, enc):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("../../../get-started/login/")
    notifications = Notification.objects.filter(to_user=request.user.pk)
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return HttpResponseRedirect("../../view-recipe/" + str(recipe.encrypt) + "/")
    users = list()
    for item in recipe.users:
        users.append(User.objects.get(pk=item))
    content = {"recipe": recipe, "users": users, "notifications": notifications}
    return render(request, "recipe/edit-people.html", content)


@login_required
def people(request, enc):
    notification_list = list()
    user_list = list()
    for i in range(50):
        if request.POST.get(str(i)) is not None and User.objects.filter(username=request.POST.get(str(i))).count() == 1:
            user = User.objects.get(username=request.POST.get(str(i)))
            notification_list.append(user.pk)
    recipe = get_object_or_404(Recipe, encrypt=enc)
    for user in recipe.users:
        for item in notification_list:
            if user == item:
                user_list.append(item)
                break
    for item in user_list:
        while item in notification_list:
            notification_list.remove(item)
    owner = recipe.users[0]
    recipe.users.clear()
    recipe.users.append(owner)
    for item in user_list:
        recipe.users.append(item)
    recipe.save()
    for item in notification_list:
        duplicates = Notification.objects.filter(recipe_id=enc, from_user=request.user.pk, to_user=item)
        if duplicates.count() == 0:
            notification = Notification(recipe_id=enc, from_user=request.user.pk, to_user=item)
            notification.save()
    return HttpResponseRedirect("../")


@login_required
def delete_recipe(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
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


@login_required
def search(query, category, request):
    if category != "All":
        recipes = Recipe.objects.filter(food_type=category)
    else:
        recipes = Recipe.objects.all()
    recipes = recipes.filter(food__icontains=query)
    recipes_query_descriptions = recipes.filter(description__contains=query)
    recipes = list(recipes)
    recipes_query_descriptions = list(recipes_query_descriptions)
    for rec in recipes_query_descriptions:
        if rec not in recipes:
            recipes.append(rec)
        for rec in recipes:
            if request.user.pk not in rec.users:
                recipes = recipes.exclude(pk=rec.pk)
    return recipes
