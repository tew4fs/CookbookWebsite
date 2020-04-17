from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Recipe
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField
import os

# Create your views here.

def index(request):
    return HttpResponseRedirect('home/')

def home(request):
    query = request.GET.get("q")
    if query:
        recipes = Recipe.objects.filter(food__contains=query)
        recipes_query_descriptions = Recipe.objects.filter(description__contains=query)
        recipes = list(recipes)
        recipes_query_descriptions = list(recipes_query_descriptions)
        for rec in recipes_query_descriptions:
            if rec not in recipes:
                recipes.append(rec)
        for rec in recipes:
            if request.user.username not in rec.users:
                recipes = recipes.exclude(pk=rec.pk)
        content = {'recipes': recipes}
    else:
        appetizers = Recipe.objects.filter(food_type="Appetizer")
        breakfast = Recipe.objects.filter(food_type="Breakfast")
        dinner = Recipe.objects.filter(food_type="Dinner")
        desserts = Recipe.objects.filter(food_type="Dessert")
        for rec in appetizers:
            if request.user.username not in rec.users:
                appetizers = appetizers.exclude(pk=rec.pk)
        appetizers = appetizers[0:4]
        for rec in breakfast:
            if request.user.username not in rec.users:
                breakfast = breakfast.exclude(pk=rec.pk)
        breakfast = breakfast[0:4]
        for rec in dinner:
            if request.user.username not in rec.users:
                dinner = dinner.exclude(pk=rec.pk)
        dinner = dinner[0:4]
        for rec in desserts:
            if request.user.username not in rec.users:
                desserts = desserts.exclude(pk=rec.pk)
        desserts = desserts[0:4]
        content = {'appetizers': appetizers, 'breakfast': breakfast, 'dinner': dinner, 'desserts': desserts}
    return render(request, 'recipe/home.html', content)

def appetizers(request):
    query = request.GET.get("q")
    if query:
        recipes = Recipe.objects.filter(food__contains=query)
        recipes_query_descriptions = Recipe.objects.filter(description__contains=query)
        recipes = list(recipes)
        recipes_query_descriptions = list(recipes_query_descriptions)
        for rec in recipes_query_descriptions:
            if rec not in recipes:
                recipes.append(rec)
        for rec in recipes:
            if request.user.username not in rec.users:
                recipes = recipes.exclude(pk=rec.pk)
        content = {'recipes': recipes}
    else:
        appetizers = Recipe.objects.filter(food_type="Appetizer")
        for rec in appetizers:
            if request.user.username not in rec.users:
                appetizers = appetizers.exclude(pk=rec.pk)
        content = {'appetizers': appetizers}
    return render(request, 'recipe/appetizers.html', content)

def breakfast(request):
    return render(request, 'recipe/breakfast.html')

def dinner(request):
    return render(request, 'recipe/dinner.html')

def desserts(request):
    return render(request, 'recipe/dessert.html')

def create_recipe(request):
    return render(request, 'recipe/create-recipe.html')

def create(request):
    food = request.POST.get('food')
    foodCat = request.POST.get('foodCat')
    desc = request.POST.get('description')
    rec = Recipe(food=food, food_type=foodCat, description=desc)
    for i in range(50):
        s = request.POST.get(str(i))
        if s is not None:
            rec.steps.append(s)
    for i in range(100, 150):
        s = request.POST.get(str(i))
        if s is not None:
            rec.ingredients.append(s)
    if request.POST.get('pic') != "":
        pic = request.FILES['pic']
        fs = FileSystemStorage()
        pic_file = fs.save(pic.name, pic)
        url = fs.url(pic_file)
        rec.picture = url
    rec.users.append(request.user.username)
    rec.save()
    return HttpResponseRedirect('../')

def view_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    content = {'recipe': recipe}
    return render(request, 'recipe/view-recipe.html', content)