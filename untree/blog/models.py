from django.contrib.auth.models import User
from django.db import models


class Teammate(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    description = models.TextField(default='Description')
    photo = models.ImageField(upload_to='team/', blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='Description')
    image = models.ImageField(upload_to='posts/')
    author = models.ForeignKey(Teammate, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField(default='Message')


class Subscription(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.name} - {self.email}'

