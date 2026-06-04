from types import SimpleNamespace

from django.shortcuts import render
from django.utils import timezone

from .models import DailyRecommendation, Event, RestaurantProfile


def home(request):
    profile = RestaurantProfile.objects.first() or SimpleNamespace(
        name="Restaurant Name",
        tagline="Fresh food, warm service",
        description="A simple Django-powered restaurant homepage.",
        phone="",
        address="",
        opening_hours="",
        map_url="",
        hero_image=None,
    )

    today = timezone.localdate()
    recommendations = DailyRecommendation.objects.filter(
        is_available=True,
        display_date=today,
    )[:6]
    upcoming_events = Event.objects.filter(
        is_published=True,
        event_date__gte=today,
    )[:3]

    return render(
        request,
        "homepage/home.html",
        {
            "profile": profile,
            "recommendations": recommendations,
            "upcoming_events": upcoming_events,
        },
    )
