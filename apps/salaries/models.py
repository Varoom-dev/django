from django.db import models
from apps.users.models import User
import django.utils.timezone as timezone
# Create your models here.
class Salary(models.Model):
    employee_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
