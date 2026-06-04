import calendar

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class RestaurantProfile(models.Model):
    name = models.CharField(max_length=120, default="Restaurant Name")
    tagline = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    opening_hours = models.CharField(max_length=180, blank=True)
    map_url = models.URLField(blank=True)
    hero_image = models.ImageField(upload_to="restaurant/", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant profile"
        verbose_name_plural = "Restaurant profile"

    def __str__(self):
        return self.name


class DailyRecommendation(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    display_date = models.DateField(default=timezone.localdate)
    is_available = models.BooleanField(default=True)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to="recommendations/", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_date", "order", "name"]

    def clean(self):
        if self.is_on_sale and self.sale_price is None:
            raise ValidationError({"sale_price": "Sale price is required for sale items."})
        if self.sale_price is not None and self.sale_price >= self.price:
            raise ValidationError({"sale_price": "Sale price should be lower than regular price."})

    def __str__(self):
        return self.name


class RestaurantPhoto(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="restaurant_photos/")
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"Restaurant photo {self.pk}"


class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=120)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({"rating": "Rating must be between 1 and 5."})

    def __str__(self):
        return f"{self.customer_name} review"


class Event(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="events/", blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["event_date", "start_time", "title"]

    def __str__(self):
        return self.title

    @property
    def display_date_en(self):
        return f"{calendar.month_abbr[self.event_date.month]} {self.event_date.day}"
