from django.db import models

# Create your models here.
class Committee(models.Model):
    name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    email = models.EmailField()
    image = models.ImageField() 