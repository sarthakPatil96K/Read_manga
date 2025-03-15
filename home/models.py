from django.db import models

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    manga_req = models.CharField(max_length=120)
    date = models.DateField()

    def __str__(self):
        return  self.name

from django.db import models


class Manga(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    description = models.TextField()
    genre = models.CharField(max_length=100)
    airing_status = models.CharField(max_length=50)
    chapter_count = models.IntegerField(null=True, blank=True)    
    rating = models.FloatField(null=True, blank=True)
    scrape_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

