from django.db import models

class User(models.Model):
    age = models.PositiveIntegerField()
    name = models.CharField()
    adress = models.PositiveIntegerField()