from django.contrib import admin

from .models import DailyRecommendation, Event, RestaurantPhoto, RestaurantProfile


@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "updated_at")

    def has_add_permission(self, request):
        if RestaurantProfile.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(DailyRecommendation)
class DailyRecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_date",
        "price",
        "sale_price",
        "is_available",
        "is_on_sale",
        "order",
    )
    list_editable = (
        "display_date",
        "price",
        "sale_price",
        "is_available",
        "is_on_sale",
        "order",
    )
    list_filter = ("display_date", "is_available", "is_on_sale")
    search_fields = ("name", "description")
    ordering = ("-display_date", "order", "name")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "start_time", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published", "event_date")
    search_fields = ("title", "description")
    ordering = ("event_date", "start_time")


@admin.register(RestaurantPhoto)
class RestaurantPhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "is_visible", "order")
    list_editable = ("is_visible", "order")
    search_fields = ("title",)
    ordering = ("order", "id")
