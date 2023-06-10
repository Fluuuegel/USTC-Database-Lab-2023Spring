from django.db import models
from PIL import Image

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=127, primary_key=True)
    passwd = models.CharField(max_length=127)
    photo = models.ImageField(upload_to='pics', null=True, blank=True)

    def save(self):
        super().save()
        img = Image.open(self.photo.path)
        # resize
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.photo.path)