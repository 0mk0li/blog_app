from django.db import models
from django.db.models.signals import pre_save, post_delete
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from .manager import UserManager
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(max_length=100, blank=True)
    profile_image = models.ImageField(blank=True, default='placeholder-pfp.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.username

    
