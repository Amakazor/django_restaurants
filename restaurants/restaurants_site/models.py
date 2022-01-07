from __future__ import annotations

from django.conf import settings
from django.db import models

class Restaurant(models.Model):
    name = models.TextField()
    slug = models.SlugField()
    description = models.TextField()
    google_maps_embed_link = models.TextField()
    image = models.ImageField(upload_to="uploads/")
    country = models.TextField()
    city = models.TextField()
    street_address = models.TextField()
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

class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    rate = models.PositiveSmallIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)