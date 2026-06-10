from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    CustomerReview,
    DailyRecommendation,
    Event,
    RestaurantPhoto,
    RestaurantProfile,
)


class ReplaceOnlyFileInput(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        file_input = forms.FileInput().render(name, None, attrs, renderer)

        if value and getattr(value, "url", None):
            current_file = format_html(
                '<a class="current-file-preview" href="{}" target="_blank" rel="noopener">'
                '<img src="{}" alt="Current uploaded image">'
                "<span>Current image</span>"
                "</a>",
                value.url,
                value.url,
            )
            return mark_safe(f"{current_file}{file_input}")

        return file_input


class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantProfile
        fields = [
            "name",
            "tagline",
            "description",
            "phone",
            "email",
            "primary_contact_method",
            "address",
            "opening_hours",
            "map_url",
            "logo",
            "show_online_order",
            "online_order_url",
            "online_order_image_left",
            "online_order_image_right",
            "show_group_reservation",
            "group_reservation_email",
            "group_reservation_background_image",
            "show_happy_hour",
            "happy_hour_schedule",
            "happy_hour_items",
            "hero_image",
            "reviews_background_image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "happy_hour_schedule": forms.Textarea(attrs={"rows": 3}),
            "happy_hour_items": forms.Textarea(attrs={"rows": 5}),
            "logo": ReplaceOnlyFileInput,
            "online_order_image_left": ReplaceOnlyFileInput,
            "online_order_image_right": ReplaceOnlyFileInput,
            "group_reservation_background_image": ReplaceOnlyFileInput,
            "hero_image": ReplaceOnlyFileInput,
            "reviews_background_image": ReplaceOnlyFileInput,
        }


class DailyRecommendationForm(forms.ModelForm):
    class Meta:
        model = DailyRecommendation
        fields = [
            "name",
            "description",
            "price",
            "is_available",
            "is_on_sale",
            "sale_price",
            "image",
            "order",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "image": ReplaceOnlyFileInput,
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "event_date",
            "start_time",
            "cover_image",
            "is_published",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "cover_image": ReplaceOnlyFileInput,
        }


class RestaurantPhotoForm(forms.ModelForm):
    class Meta:
        model = RestaurantPhoto
        fields = [
            "title",
            "image",
            "is_visible",
            "order",
        ]
        widgets = {
            "image": ReplaceOnlyFileInput,
        }


class CustomerReviewForm(forms.ModelForm):
    customer_name = forms.CharField(label="Display name")
    quote = forms.CharField(
        label="Review text",
        widget=forms.Textarea(attrs={"rows": 4}),
    )
    rating = forms.IntegerField(label="Displayed rating", min_value=1, max_value=5)

    class Meta:
        model = CustomerReview
        fields = [
            "customer_name",
            "quote",
            "rating",
            "is_visible",
            "order",
        ]
