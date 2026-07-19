from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUser(AbstractUser):
    class AccType(models.TextChoices):
        LISTER = 'lister'
        SEEKER = 'seeker'

    class Gender(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        OTHERS = 'others'

    account_type = models.CharField(max_length=10, choices= AccType.choices)
    gender = models.CharField(max_length = 7, choices = Gender.choices)
    dob = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    agreed_to_terms = models.BooleanField(default=False)
    agreed_to_terms_at = models.DateTimeField(null=True, blank=True)
    terms_version = models.CharField(max_length=20, blank=True)
    agreed_to_privacy = models.BooleanField(default=False)
    agreed_to_privacy_at = models.DateTimeField(null=True, blank=True)
    privacy_version = models.CharField(max_length=20, blank=True)
    agreed_to_lister_onboarding = models.BooleanField(default=False)
    agreed_to_lister_onboarding_at = models.DateTimeField(null=True, blank=True)
    lister_onboarding_version = models.CharField(max_length=20, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'profile'
    )
    profile_image = models.ImageField(upload_to = 'profile/images/', blank = True, null = True)
    def __str__(self):
        return f"{self.user.username}'s profile"