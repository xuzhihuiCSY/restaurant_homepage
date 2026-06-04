from django.contrib import admin

from .models import Category, Event, MenuItem, RestaurantProfile


@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "updated_at")

    def has_add_permission(self, request):
        if RestaurantProfile.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order", "name")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "base_price",
        "sale_price",
        "is_available",
        "is_featured",
        "is_on_sale",
        "order",
    )
    list_editable = (
        "base_price",
        "sale_price",
        "is_available",
        "is_featured",
        "is_on_sale",
        "order",
    )
    list_filter = ("category", "is_available", "is_featured", "is_on_sale")
    search_fields = ("name", "description")
    ordering = ("category__order", "order", "name")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "start_time", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published", "event_date")
    search_fields = ("title", "description")
    ordering = ("event_date", "start_time")
