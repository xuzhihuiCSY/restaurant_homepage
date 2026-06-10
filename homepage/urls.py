from django.urls import path

from . import views

app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("restaurant/", views.restaurant_detail, name="restaurant_detail"),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
    path("owner/photos/new/", views.restaurant_photo_create, name="photo_create"),
    path("owner/photos/<int:pk>/edit/", views.restaurant_photo_edit, name="photo_edit"),
    path(
        "owner/photos/<int:pk>/delete/",
        views.restaurant_photo_delete,
        name="photo_delete",
    ),
    path("owner/reviews/new/", views.review_create, name="review_create"),
    path("owner/reviews/<int:pk>/edit/", views.review_edit, name="review_edit"),
    path("owner/reviews/<int:pk>/delete/", views.review_delete, name="review_delete"),
    path(
        "owner/recommendations/new/",
        views.recommendation_create,
        name="recommendation_create",
    ),
    path(
        "owner/recommendations/<int:pk>/edit/",
        views.recommendation_edit,
        name="recommendation_edit",
    ),
    path(
        "owner/recommendations/<int:pk>/delete/",
        views.recommendation_delete,
        name="recommendation_delete",
    ),
    path("owner/events/new/", views.event_create, name="event_create"),
    path("owner/events/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("owner/events/<int:pk>/delete/", views.event_delete, name="event_delete"),
]
