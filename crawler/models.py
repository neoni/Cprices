from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)
    href = models.CharField(max_length=500)
    img = models.CharField(max_length=500)
    types = models.CharField(max_length=8)
    prices = models.CharField(max_length=400, blank=True, null=True)
    dates = models.CharField(max_length=400, blank=True, null=True)
    user = models.ForeignKey(User)
    is_updated = models.BooleanField(default=False)
    updated_s = models.CharField(max_length=300, blank=True, null=True)
