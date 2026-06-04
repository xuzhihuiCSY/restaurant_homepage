from django import forms

from .models import (
    CustomerReview,
    DailyRecommendation,
    Event,
    RestaurantPhoto,
    RestaurantProfile,
)


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
            "show_online_order",
            "online_order_url",
            "online_order_image_left",
            "online_order_image_right",
            "hero_image",
            "reviews_background_image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class DailyRecommendationForm(forms.ModelForm):
    class Meta:
        model = DailyRecommendation
        fields = [
            "name",
            "description",
            "price",
            "display_date",
            "is_available",
            "is_on_sale",
            "sale_price",
            "image",
            "order",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "display_date": forms.DateInput(attrs={"type": "date"}),
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
