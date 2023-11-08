from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username

class MentalState(models.Model):
    mood = models.CharField(max_length=100)
    cause = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.mood} because {self.cause}'