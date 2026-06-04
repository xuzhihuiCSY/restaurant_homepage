from django.core.exceptions import ValidationError
from django.db import models


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


class Category(models.Model):
    name = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to="menu/", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category__order", "order", "name"]

    def clean(self):
        if self.is_on_sale and self.sale_price is None:
            raise ValidationError({"sale_price": "Sale price is required for sale items."})
        if self.sale_price is not None and self.sale_price >= self.base_price:
            raise ValidationError({"sale_price": "Sale price should be lower than base price."})

    def __str__(self):
        return self.name


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
