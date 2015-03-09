from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Site(models.Model):
    user = models.ForeignKey(User)
    domain = models.CharField(max_length = 255)


