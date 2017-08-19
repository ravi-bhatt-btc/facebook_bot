from django.db import models

# Create your models here.

class Users(models.Model):
    sender_id = models.CharField(unique=True, max_length=100)
    name = models.CharField(unique=True, max_length=80)
    email = models.EmailField(unique=True, max_length=100, null=True)
    phone = models.CharField(unique=True, max_length=20, null=True)

    def __str__(self):
        return self.name