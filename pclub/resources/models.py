from django.db import models

# Create your models here.
class Tags(models.Model):
    tag = models.CharField(max_length=220)

    def __str__(self):
        return self.tag

class Resources(models.Model):
    title = models.CharField(max_length=300)
    resource_file = models.FileField(upload_to="resources/uploads", null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=500, default="")
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title

    def get_tags(self):
        tag_names=[]    
        tags = self.tags.all()
        for i in tags:
            tag_names.append(i.tag)
        return set(tag_names)