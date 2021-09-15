from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

class Note(models.Model):
    title = models.CharField(max_length=30, unique=True)
    note_text = models.CharField(max_length=1000, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title.capitalize()
