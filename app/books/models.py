from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=64)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Ban(models.Model):
    book = models.ForeignKey(Book,related_name='bans', on_delete=models.CASCADE)
    type_of_ban = models.CharField(max_length=64)
    secondary_author = models.CharField(max_length=256, blank=True, null=True)
    illustrator = models.CharField(max_length=128, blank=True, null=True)
    translator = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=32)
    district = models.CharField(max_length=100)
    date_of_challenge_removal = models.CharField(max_length=32, blank=True, null=True)
    origin_of_challenge = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.district}, {self.state}"
