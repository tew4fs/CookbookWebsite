
from django.db import models

class Notification(models.Model):
    recipe_id = models.CharField(max_length=100, default="")
    from_user = models.CharField(max_length=80, default="")
    to_user = models.CharField(max_length=80, default="")
    read = models.BooleanField(default=False)

class Unverified(models.Model):
    user = models.CharField(max_length=80, default="")