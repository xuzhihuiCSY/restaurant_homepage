from django import forms

from .models import DailyRecommendation, Event, RestaurantProfile


class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantProfile
        fields = [
            "name",
            "tagline",
            "description",
            "phone",
            "address",
            "opening_hours",
            "map_url",
            "hero_image",
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
