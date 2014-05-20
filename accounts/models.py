from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ClientId(models.Model):
    cid = models.CharField(max_length=32)
    user = models.ForeignKey(User, db_index=True)

