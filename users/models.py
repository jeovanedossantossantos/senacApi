from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

# default="user"
# https://docs.djangoproject.com/en/4.0/ref/models/fields/#choices
class UsersModel(AbstractUser):
    TIPO_CHOICES = [
        ('root', 'Root'),
        ('client', 'Client'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tipo=models.CharField(max_length=10, choices=TIPO_CHOICES,default='client')
    suspenso = models.BooleanField(default=False)
    email = models.EmailField(unique=True)