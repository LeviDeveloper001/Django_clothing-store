from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# class ShoppingCart(models.Model):
#     pass

class ProfileManager(models.Manager):
    pass

class Profile(models.Model):
    user=models.OneToOneField('User', on_delete=models.CASCADE)
    description=models.TextField(max_length=1000, null=True, editable=True)
    profile_image=models.ImageField(upload_to='static/images/accounts/profile_images/', null=True, editable=True)
    
    manager=ProfileManager()


class CustomUserManager(UserManager):
    def _create_user(self, username, email=None, password=None, **extra_fields):
        user=super()._create_user(username, email=email, password=password, **extra_fields)
        if user:
            profile = Profile(user=user)
            profile.save()

class User(AbstractUser):
    manager=CustomUserManager()
    objects=CustomUserManager()







