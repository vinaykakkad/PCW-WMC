from django.db import models
# Create your models here.


class Announcements(models.Model):
    announcement = models.TextField()

    def __str__(self):
        return str(self.pk)
