from django.db import models

# Create your models here.

class Thoughts(models.Model):
    thought = models.TextField()
    author = models.CharField(max_length=300, default="Anonymous")

    def __str__(self):
        return self.thought
    # def get_author(self):
    #     return self.author

class  Announcements(models.Model):
    announcemnt = models.TextField()

    def __str__(self):
        return self.announcemnt