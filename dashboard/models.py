import os
import random
from django.contrib.auth.models import User

from django.db import models


def update_filename(instance, filename):
    path = 'cover'
    fileName, fileExtension = os.path.splitext(filename)
    format = str(random.getrandbits(128)) + fileExtension
    return os.path.join(path, format)

# Create your models here.

class books(models.Model):
    author              = models.CharField(max_length=60)
    name                = models.CharField(max_length=60)
    description         = models.TextField(max_length=180)
    price               = models.CharField(max_length=60)
    cover               = models.ImageField(upload_to=update_filename,default='default.png',blank=True,null=True,)
    user_id             = models.ManyToManyField(User,blank=True)


    def __str__(self):
        return self.name