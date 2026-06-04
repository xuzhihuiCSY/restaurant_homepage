from types import SimpleNamespace

from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone

from .models import Category, Event, MenuItem, RestaurantProfile


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

    visible_items = MenuItem.objects.filter(is_available=True)
    categories = Category.objects.prefetch_related(
        Prefetch("items", queryset=visible_items.order_by("order", "name"))
    )
    featured_items = visible_items.filter(is_featured=True).select_related("category")[:6]
    sale_items = (
        visible_items.filter(is_on_sale=True, sale_price__isnull=False)
        .select_related("category")
        [:4]
    )
    upcoming_events = Event.objects.filter(
        is_published=True,
        event_date__gte=timezone.localdate(),
    )[:3]

    return render(
        request,
        "homepage/home.html",
        {
            "profile": profile,
            "categories": categories,
            "featured_items": featured_items,
            "sale_items": sale_items,
            "upcoming_events": upcoming_events,
        },
    )
