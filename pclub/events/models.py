from django.db import models

# Create your models here.
class Events(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    date = models.DateField()

class Images(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="images", )
    image = models.ImageField(upload_to="events/images")

    def get_url(self):
        return self.image.url