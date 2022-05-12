from django.db import models
from django.contrib.auth.models import AbstractUser

class CustumUser(models.Model):
    userposition = models.CharField(max_length=200)
    REQUIRED_FIELDS = ['userposition']

    # def __str__(self):
    #     return self.user.username
