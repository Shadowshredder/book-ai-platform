from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title