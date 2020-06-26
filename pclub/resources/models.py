from django.db import models


# Create your models here.
class Tags(models.Model):
    tag = models.CharField(max_length=220)

    def __str__(self):
        return self.tag

class Resources(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField(max_length=500, default="")
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title

class Files(models.Model):
    name = models.CharField(max_length=220, default="",)
    resource = models.ForeignKey(Resources, on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    resource_file = models.FileField(upload_to="resouces/uploads")
    def __str__(self):
        return self.name

class Links(models.Model):
    name = models.CharField(max_length=220, default="")
    resource = models.ForeignKey(Resources, on_delete=models.CASCADE, related_name="links", null=True, blank=True) 
    resource_links = models.CharField(max_length=300)

    def __str__(self):
        return self.resource_links
