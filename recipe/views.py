from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField
from django.contrib import messages
from django.contrib.auth.models import User 
from login.models import Notification, Unverified
from .models import Recipe
import os

# Create your views here.

def index(request):
    return HttpResponseRedirect('home/')

def home(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "All", request)
        content = {'recipes': recipes}
    else:
        appetizers = Recipe.objects.filter(food_type="Appetizer")
        breakfast = Recipe.objects.filter(food_type="Breakfast")
        dinner = Recipe.objects.filter(food_type="Dinner")
        desserts = Recipe.objects.filter(food_type="Dessert")
        for rec in appetizers:
            if request.user.pk not in rec.users:
                appetizers = appetizers.exclude(pk=rec.pk)
        appetizers = appetizers[0:4]
        for rec in breakfast:
            if request.user.pk not in rec.users:
                breakfast = breakfast.exclude(pk=rec.pk)
        breakfast = breakfast[0:4]
        for rec in dinner:
            if request.user.pk not in rec.users:
                dinner = dinner.exclude(pk=rec.pk)
        dinner = dinner[0:4]
        for rec in desserts:
            if request.user.pk not in rec.users:
                desserts = desserts.exclude(pk=rec.pk)
        desserts = desserts[0:4]
        content = {'appetizers': appetizers, 'breakfast': breakfast, 'dinner': dinner, 'desserts': desserts, 'notifications': notifications,}
    return render(request, 'recipe/home.html', content)

def appetizers(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "Appetizer", request)
        content = {'recipes': recipes}
    else:
        appetizers = Recipe.objects.filter(food_type="Appetizer")
        for rec in appetizers:
            if request.user.pk not in rec.users:
                appetizers = appetizers.exclude(pk=rec.pk)
        content = {'appetizers': appetizers, 'notifications': notifications}
    return render(request, 'recipe/appetizers.html', content)

def breakfast(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "Breakfast", request)
        content = {'recipes': recipes}
    else:
        breakfast = Recipe.objects.filter(food_type="Breakfast")
        for rec in breakfast:
            if request.user.pk not in rec.users:
                breakfast = breakfast.exclude(pk=rec.pk)
        content = {'breakfast': breakfast, 'notifications': notifications}
    return render(request, 'recipe/breakfast.html', content)

def dinner(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "Dinner", request)
        content = {'recipes': recipes}
    else:
        dinner = Recipe.objects.filter(food_type="Dinner")
        for rec in dinner:
            if request.user.pk not in rec.users:
                dinner = dinner.exclude(pk=rec.pk)
        content = {'dinner': dinner, 'notifications': notifications}
    return render(request, 'recipe/dinner.html', content)

def desserts(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    query = request.GET.get("q")
    if query:
        recipes = search(query, "Dessert", request)
        content = {'recipes': recipes}
    else:
        desserts = Recipe.objects.filter(food_type="Dessert")
        for rec in desserts:
            if request.user.pk not in rec.users:
                desserts = desserts.exclude(pk=rec.pk)
        content = {'desserts': desserts, 'notifications': notifications}
    return render(request, 'recipe/dessert.html', content)

def create_recipe(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../get-started/login/')
    if len(Unverified.objects.filter(user=request.user.pk)) > 0:
        return HttpResponseRedirect('../')
    notifications = Notification.objects.filter(to_user=request.user.username)
    content = {'notifications': notifications}
    return render(request, 'recipe/create-recipe.html', content)

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
        pic_str = str(pic)
        pic_str = pic_str[len(pic_str)-4:len(pic_str)]
        if pic_str == '.png' or pic_str == '.jpg' or pic_str == 'jpeg' or pic_str == '.PNG' or pic_str == '.JPG' or pic_str == 'JPEG':
            fs = FileSystemStorage()
            pic_file = fs.save(pic.name, pic)
            url = fs.url(pic_file)
            rec.picture = url
    rec.users.append(request.user.pk)
    rec.save()
    return HttpResponseRedirect('../')

def view_recipe(request, enc):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    recipe = get_object_or_404(Recipe, encrypt=enc)
    owner = False
    if recipe.users[0] == request.user.pk:
        owner = True
    content = {'recipe': recipe, 'notifications': notifications, 'is_owner': owner}
    return render(request, 'recipe/view-recipe.html', content)

def edit_recipe(request, enc):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return HttpResponseRedirect('../../view-recipe/' + str(recipe.encrypt) +'/')
    content = {'recipe': recipe, 'notifications': notifications}
    return render(request, 'recipe/edit-recipe.html', content)

def edit(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return HttpResponseRedirect('../../../view-recipe/' + str(recipe.encrypt) +'/')
    recipe.food = request.POST.get('food')
    recipe.food_type = request.POST.get('foodCat')
    recipe.description = request.POST.get('description')
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
    print(request.POST.get('pic'))
    if request.POST.get('pic') != "":
        pic = request.FILES['pic']
        pic_str = str(pic)
        pic_str = pic_str[len(pic_str)-4:len(pic_str)]
        if pic_str == '.png' or pic_str == '.jpg' or pic_str == 'jpeg' or pic_str == '.PNG' or pic_str == '.JPG' or pic_str == 'JPEG':
            fs = FileSystemStorage()
            pic_file = fs.save(pic.name, pic)
            url = fs.url(pic_file)
            recipe.picture = url
    recipe.save()
    return HttpResponseRedirect('../../../view-recipe/' + str(recipe.encrypt) +'/')

def remove_picture(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return redirect('home')
    recipe.picture = ""
    recipe.save()
    return redirect('edit_recipe', enc=enc)

def edit_people(request, enc):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('../../../get-started/login/')
    notifications = Notification.objects.filter(to_user=request.user.pk)
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return HttpResponseRedirect('../../view-recipe/' + str(recipe.encrypt) +'/')
    users = list()
    for item in recipe.users:
        users.append(User.objects.get(pk=item))
    content = {'recipe': recipe, 'users': users, 'notifications': notifications}
    return render(request, 'recipe/edit-people.html', content)

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
    return HttpResponseRedirect('../')

def delete_recipe(request, enc):
    recipe = get_object_or_404(Recipe, encrypt=enc)
    if request.user.pk != recipe.users[0]:
        return HttpResponseRedirect('../../view-recipe/' + str(recipe.encrypt) +'/')
    recipe.delete()
    return HttpResponseRedirect('../../')

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
    return HttpResponseRedirect('../../')

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