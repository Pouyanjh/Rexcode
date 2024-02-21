from django.db import models

class Talk(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)