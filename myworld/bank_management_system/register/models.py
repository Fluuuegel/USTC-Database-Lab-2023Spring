from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=127, primary_key=True)
    passwd = models.CharField(max_length=127)
    photo = models.ImageField(upload_to='pics', null=True, blank=True)