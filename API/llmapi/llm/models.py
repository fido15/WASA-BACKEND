from django.db import models

# Create your models here.
from django.db import models

class NewSite(models.Model):
    link = models.URLField(max_length=200)  
    reliability = models.FloatField()  
    source = models.TextField(max_length=200)

    def __str__(self):
        return self.link

class Category(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name

class RssData(models.Model):
    title = models.TextField()  
    link = models.URLField(max_length=200)  
    published = models.TextField()
    updated = models.TextField()
    country = models.CharField(max_length=100)  
    image = models.JSONField()
    summary = models.TextField()
    categories = models.ManyToManyField(Category, related_name="articles")  


    def __str__(self):
        return self.title

