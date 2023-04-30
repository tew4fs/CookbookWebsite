from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
import os

# Create your models here.


def get_image_path(instance, filename):
    return os.path.join("photos", filename)


class Recipe(models.Model):
    food = models.CharField(max_length=80, default="")
    food_type = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=300)
    picture = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    encrypt = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    cook_time = models.IntegerField(default=0)
    serves = models.IntegerField(default=0)
    ingredients = ArrayField(
        models.CharField(max_length=80),
        default=list,
        size=100,
    )
    steps = ArrayField(
        models.CharField(max_length=300),
        default=list,
        size=100,
    )
    users = ArrayField(
        models.IntegerField(default=-1),
        default=list,
        size=1000,
    )
