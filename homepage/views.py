from types import SimpleNamespace

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    DailyRecommendationForm,
    EventForm,
    RestaurantPhotoForm,
    RestaurantProfileForm,
)
from .models import DailyRecommendation, Event, RestaurantPhoto, RestaurantProfile


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
    restaurant_photos = RestaurantPhoto.objects.filter(is_visible=True)[:6]

    return render(
        request,
        "homepage/home.html",
        {
            "profile": profile,
            "restaurant_photos": restaurant_photos,
            "recommendations": recommendations,
            "upcoming_events": upcoming_events,
        },
    )


@staff_member_required
def owner_dashboard(request):
    profile = RestaurantProfile.objects.first()
    if profile is None:
        profile = RestaurantProfile.objects.create()

    if request.method == "POST":
        profile_form = RestaurantProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Restaurant homepage details updated.")
            return redirect("homepage:owner_dashboard")
    else:
        profile_form = RestaurantProfileForm(instance=profile)

    today = timezone.localdate()
    restaurant_photos = RestaurantPhoto.objects.all()[:12]
    recommendations = DailyRecommendation.objects.filter(display_date__gte=today)[:12]
    upcoming_events = Event.objects.filter(event_date__gte=today)[:8]

    return render(
        request,
        "homepage/owner/dashboard.html",
        {
            "profile_form": profile_form,
            "restaurant_photos": restaurant_photos,
            "recommendations": recommendations,
            "upcoming_events": upcoming_events,
            "today": today,
        },
    )


@staff_member_required
def recommendation_create(request):
    return _save_model_form(
        request,
        DailyRecommendationForm,
        "homepage/owner/form.html",
        "Add today's recommended dish",
    )


@staff_member_required
def restaurant_photo_create(request):
    return _save_model_form(
        request,
        RestaurantPhotoForm,
        "homepage/owner/form.html",
        "Add restaurant photo",
    )


@staff_member_required
def restaurant_photo_edit(request, pk):
    photo = get_object_or_404(RestaurantPhoto, pk=pk)
    return _save_model_form(
        request,
        RestaurantPhotoForm,
        "homepage/owner/form.html",
        "Edit restaurant photo",
        instance=photo,
    )


@staff_member_required
def restaurant_photo_delete(request, pk):
    photo = get_object_or_404(RestaurantPhoto, pk=pk)
    return _confirm_delete(
        request,
        photo,
        "Delete restaurant photo",
        f"Delete {photo} from the homepage photo display?",
    )


@staff_member_required
def recommendation_edit(request, pk):
    recommendation = get_object_or_404(DailyRecommendation, pk=pk)
    return _save_model_form(
        request,
        DailyRecommendationForm,
        "homepage/owner/form.html",
        "Edit recommended dish",
        instance=recommendation,
    )


@staff_member_required
def recommendation_delete(request, pk):
    recommendation = get_object_or_404(DailyRecommendation, pk=pk)
    return _confirm_delete(
        request,
        recommendation,
        "Delete recommended dish",
        f"Delete {recommendation.name} from the owner controls?",
    )


@staff_member_required
def event_create(request):
    return _save_model_form(
        request,
        EventForm,
        "homepage/owner/form.html",
        "Add event",
    )


@staff_member_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return _save_model_form(
        request,
        EventForm,
        "homepage/owner/form.html",
        "Edit event",
        instance=event,
    )


@staff_member_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return _confirm_delete(
        request,
        event,
        "Delete event",
        f"Delete {event.title} from the owner controls?",
    )


def _save_model_form(request, form_class, template_name, title, instance=None):
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"{title} saved.")
            return redirect("homepage:owner_dashboard")
    else:
        form = form_class(instance=instance)

    return render(
        request,
        template_name,
        {
            "form": form,
            "title": title,
            "cancel_url": "homepage:owner_dashboard",
        },
    )


def _confirm_delete(request, instance, title, message):
    if request.method == "POST":
        instance.delete()
        messages.success(request, f"{title} completed.")
        return redirect("homepage:owner_dashboard")

    return render(
        request,
        "homepage/owner/confirm_delete.html",
        {
            "title": title,
            "message": message,
            "cancel_url": "homepage:owner_dashboard",
        },
    )
