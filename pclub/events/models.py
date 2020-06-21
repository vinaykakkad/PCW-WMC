from datetime import datetime
import pytz

from django.db import models

# Create your models here.
# class Tags(models.Model):
#     tag_name = 

class Events(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    registration_link = models.CharField(max_length=300, default="")

    def get_tzinfo_current(self):
        return datetime.now(tz=self.start_date.tzinfo)

    def is_registration_active(self):
        if self.get_tzinfo_current() < self.start_date:
            return True
        else:
            return False

class Images(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="events/images")

    def get_url(self):
        return self.image.url