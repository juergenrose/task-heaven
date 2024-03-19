from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, max_length=100, on_delete=models.CASCADE, null=True)
