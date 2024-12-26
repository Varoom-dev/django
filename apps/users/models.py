from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
import json

class User(AbstractUser):
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):  # Ensures password isn't hashed multiple times
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission_json = models.JSONField()  # Store permissions in JSON format

    def __str__(self):
        return f"Permissions for {self.role.name}"

class RoleUser(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_users')

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
