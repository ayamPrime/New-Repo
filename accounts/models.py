from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    class AccType(models.TextChoices):
        STUDENT = 'student'
        AGENT = 'agent'
    
    class Gender(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        OTHERS = 'others'

    account_type = models.CharField(max_length=7, choices= AccType.choices)
    gender = models.CharField(max_length = 7, choices = Gender.choices)