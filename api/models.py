from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='faraz',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='khan',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class SpamNumber(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    marked_as_spam = models.BooleanField(default=True)
    
    def __str__(self):
        return self.phone_number