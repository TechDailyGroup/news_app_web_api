from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):

    GENDERS = (("M", "Male"), ("F", "Female"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=16, choices=GENDERS, default="M")
    nickname = models.CharField(max_length=32)

    def __str__(self):
        return self.user.username
