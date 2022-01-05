from django.conf import settings
from django.db import models

class Restaurant(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    description = models.TextField()
    google_maps_embed_link = models.TextField()
    image = models.ImageField()
    country = models.TextField()
    city = models.TextField()
    street_address = models.TextField()
    is_active = models.BooleanField(default=False)

class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    rate = models.PositiveSmallIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)