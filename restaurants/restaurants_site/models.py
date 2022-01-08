from __future__ import annotations

from django.conf import settings
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=512)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    google_maps_embed_link = models.CharField(null=True, max_length=512, blank= True)
    image = models.ImageField()
    country = models.CharField(max_length=512)
    city = models.CharField(max_length=512)
    street_address = models.CharField(max_length=512)
    is_active = models.BooleanField(default=False)

    @property
    def average_rate(self) -> int:
        return int(Review.objects.filter(restaurant = self).aggregate(models.Avg('rate'))['rate__avg'] or 0)

    @property
    def stars_full(self) -> str:
        return "★" * self.average_rate

    @property
    def stars_empty(self) -> str:
        return "★" * (5 - self.average_rate)

    @property
    def excerpt(self) -> str:
        return self.description[0:200] + ('' if len(self.description) <= 200 else '...')

    @property
    def reviews(self):
        return Review.objects.filter(restaurant = self)

    def save(self, *args, **kwargs):
         if not self.google_maps_embed_link:
              self.google_maps_embed_link = None
         super(Restaurant, self).save(*args, **kwargs)

class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    rate = models.PositiveSmallIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def stars_full(self) -> str:
        return "★" * self.rate

    @property
    def stars_empty(self) -> str:
        return "★" * (5 - self.rate)