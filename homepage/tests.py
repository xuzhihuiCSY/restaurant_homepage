import os
import shutil
import tempfile
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone

from .models import CustomerReview, DailyRecommendation, Event, RestaurantPhoto, RestaurantProfile


class HomePageTests(TestCase):
    def test_homepage_renders_successfully(self):
        response = self.client.get(reverse("homepage:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurant Name")
        self.assertContains(response, reverse("homepage:restaurant_detail"))
        self.assertContains(response, "Restaurant photos")
        self.assertContains(response, "Chef recommended dishes")
        self.assertContains(response, "What guests say")

    def test_restaurant_detail_page_renders_profile_only(self):
        RestaurantProfile.objects.create(
            name="Detail Restaurant",
            description="A focused restaurant detail page.",
            address="123 Main Street, Seattle, WA",
            map_url="https://maps.example.com/detail-restaurant",
            logo="restaurant/logo.png",
            hero_image="restaurant/hero.jpg",
        )
        DailyRecommendation.objects.create(name="Hidden Dish", price="12.50")
        Event.objects.create(
            title="Hidden Event",
            event_date=timezone.localdate() + timedelta(days=1),
            is_published=True,
        )

        response = self.client.get(reverse("homepage:restaurant_detail"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail Restaurant")
        self.assertContains(response, "A focused restaurant detail page.")
        self.assertContains(response, "123 Main Street, Seattle, WA")
        self.assertContains(response, "restaurant/logo.png")
        self.assertContains(response, "restaurant/hero.jpg")
        self.assertContains(response, "maps.google.com/maps")
        self.assertContains(response, 'href="https://maps.example.com/detail-restaurant"')
        self.assertNotContains(response, "Chef recommended dishes")
        self.assertNotContains(response, "Upcoming dates")
        self.assertNotContains(response, "Hidden Dish")
        self.assertNotContains(response, "Hidden Event")

    def test_recommendation_renders_on_homepage_without_date_setup(self):
        DailyRecommendation.objects.create(
            name="Lunch Special",
            price="12.50",
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "Lunch Special")

    def test_happy_hour_section_renders_when_visible(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            show_happy_hour=True,
            happy_hour_schedule="Monday-Friday\n4:00 PM - 6:00 PM",
            happy_hour_items="Wings\nDraft beer\nKaraoke snacks",
        )

        response = self.client.get(reverse("homepage:home"))
        content = response.content.decode()

        self.assertContains(response, 'id="happy-hour"')
        self.assertContains(response, "Happy hour")
        self.assertContains(response, "Monday-Friday")
        self.assertContains(response, "4:00 PM - 6:00 PM")
        self.assertContains(response, "Wings")
        self.assertContains(response, "Draft beer")
        self.assertLess(content.index("Chef recommended dishes"), content.index('id="happy-hour"'))
        self.assertLess(content.index('id="happy-hour"'), content.index("What guests say"))

    def test_happy_hour_section_stays_hidden_when_disabled(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            show_happy_hour=False,
            happy_hour_schedule="Monday-Friday 4:00 PM - 6:00 PM",
            happy_hour_items="Wings",
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertNotContains(response, 'id="happy-hour"')
        self.assertNotContains(response, "Monday-Friday 4:00 PM - 6:00 PM")

    def test_happy_hour_schedule_required_when_section_visible(self):
        profile = RestaurantProfile(
            name="Test Restaurant",
            show_happy_hour=True,
            happy_hour_items="Wings",
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_happy_hour_items_required_when_section_visible(self):
        profile = RestaurantProfile(
            name="Test Restaurant",
            show_happy_hour=True,
            happy_hour_schedule="Monday-Friday 4:00 PM - 6:00 PM",
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_event_date_renders_in_english(self):
        Event.objects.create(
            title="Karaoke Night",
            event_date=date(2099, 1, 5),
            is_published=True,
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "Jan 5")
        self.assertNotContains(response, "1月")

    def test_event_cover_image_renders_as_card_background(self):
        Event.objects.create(
            title="Live Band",
            event_date=date(2099, 2, 6),
            cover_image="events/live-band.jpg",
            is_published=True,
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "has-event-image")
        self.assertContains(response, "events/live-band.jpg")

    def test_homepage_event_cards_render_nearest_five_events(self):
        start_date = timezone.localdate() + timedelta(days=35)
        for index in range(6):
            Event.objects.create(
                title=f"Future Event {index + 1}",
                event_date=start_date + timedelta(days=index),
                is_published=True,
            )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "Future Event 1")
        self.assertContains(response, "Future Event 5")
        self.assertNotContains(response, "Future Event 6")

    def test_event_calendar_renders_current_month_events(self):
        Event.objects.create(
            title="Calendar Night",
            description="Late set and snacks.",
            event_date=timezone.localdate(),
            is_published=True,
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "event-calendar")
        self.assertContains(response, "Calendar Night")
        self.assertContains(response, "calendar-day-button")
        self.assertContains(response, "calendar-event-details")
        self.assertContains(response, "Late set and snacks.")
        self.assertContains(response, 'id="event-modal"')

    def test_visible_customer_review_renders_between_recommendations_and_events(self):
        CustomerReview.objects.create(
            customer_name="Alex",
            quote="Great karaoke night and friendly staff.",
            rating=5,
            is_visible=True,
        )

        response = self.client.get(reverse("homepage:home"))
        content = response.content.decode()

        self.assertContains(response, "Great karaoke night and friendly staff.")
        self.assertLess(content.index("Chef recommended dishes"), content.index("What guests say"))
        self.assertLess(content.index("What guests say"), content.index("Upcoming dates"))

    def test_reviews_section_uses_uploaded_background_image(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            reviews_background_image="restaurant/reviews.jpg",
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "has-review-background")
        self.assertContains(response, "restaurant/reviews.jpg")

    def test_profile_email_and_email_contact_preference_render(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            phone="555-0100",
            email="hello@example.com",
            primary_contact_method=RestaurantProfile.CONTACT_EMAIL,
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, 'href="mailto:hello@example.com"')
        self.assertContains(response, "Email us")
        self.assertContains(response, "hello@example.com")

    def test_restaurant_logo_renders_on_homepage(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            logo="restaurant/logo.png",
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "restaurant/logo.png")
        self.assertContains(response, "Test Restaurant logo")

    def test_online_order_section_renders_when_visible_with_url(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            show_online_order=True,
            online_order_url="https://order.example.com/menu",
            online_order_image_left="restaurant/order-left.jpg",
            online_order_image_right="restaurant/order-right.jpg",
        )

        response = self.client.get(reverse("homepage:home"))
        content = response.content.decode()

        self.assertContains(response, "Order Online")
        self.assertContains(response, 'href="https://order.example.com/menu"')
        self.assertContains(response, "restaurant/order-left.jpg")
        self.assertContains(response, "restaurant/order-right.jpg")
        self.assertLess(content.index("What guests say"), content.index('id="order-online"'))
        self.assertLess(content.index('id="order-online"'), content.index("Upcoming dates"))

    def test_online_order_url_required_when_section_visible(self):
        profile = RestaurantProfile(name="Test Restaurant", show_online_order=True)

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_group_reservation_section_renders_when_visible(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            show_group_reservation=True,
            group_reservation_email="manager@example.com",
            group_reservation_background_image="restaurant/group-reservation.jpg",
        )

        response = self.client.get(reverse("homepage:home"))
        content = response.content.decode()

        self.assertContains(response, 'id="group-reservation"')
        self.assertContains(response, "Group reservation")
        self.assertContains(response, "BOOK A PARTY")
        self.assertContains(response, "restaurant/group-reservation.jpg")
        self.assertContains(
            response,
            'href="mailto:manager@example.com?subject=Group%20reservation%20request"',
        )
        self.assertLess(content.index('id="group-reservation"'), content.index("Upcoming dates"))

    def test_group_reservation_email_required_when_section_visible(self):
        profile = RestaurantProfile(
            name="Test Restaurant",
            show_group_reservation=True,
            group_reservation_background_image="restaurant/group-reservation.jpg",
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_group_reservation_background_required_when_section_visible(self):
        profile = RestaurantProfile(
            name="Test Restaurant",
            show_group_reservation=True,
            group_reservation_email="manager@example.com",
        )

        with self.assertRaises(ValidationError):
            profile.full_clean()


class OwnerControlsTests(TestCase):
    def test_owner_dashboard_requires_staff_login(self):
        response = self.client.get(reverse("homepage:owner_dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_staff_can_open_owner_dashboard(self):
        user = self._create_staff_user()
        self.client.force_login(user)

        response = self.client.get(reverse("homepage:owner_dashboard"))
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Homepage display controls")
        self.assertContains(response, "Restaurant photo display")
        self.assertContains(response, "Review highlights")
        self.assertContains(response, "Logo")
        self.assertContains(response, "Online order")
        self.assertContains(response, "Happy hour")
        self.assertContains(response, "Group reservation")
        self.assertContains(response, "Reviews background image")
        self.assertLess(content.index("Homepage details"), content.index("Online order"))
        self.assertLess(content.index("Online order"), content.index("Happy hour"))
        self.assertLess(content.index("Happy hour"), content.index("Group reservation"))
        self.assertLess(content.index("Group reservation"), content.index("Review highlights"))
        self.assertLess(content.index("Review highlights"), content.index("Reviews background image"))
        self.assertLess(content.index("Reviews background image"), content.index("Restaurant photo display"))

    def test_owner_image_fields_do_not_show_clear_checkbox(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            logo="restaurant/logo.png",
        )
        user = self._create_staff_user()
        self.client.force_login(user)

        response = self.client.get(reverse("homepage:owner_dashboard"))

        self.assertContains(response, "current-file-preview")
        self.assertContains(response, "Current image")
        self.assertContains(response, 'src="/media/restaurant/logo.png"')
        self.assertContains(response, "restaurant/logo.png")
        self.assertNotContains(response, "Clear")
        self.assertNotContains(response, 'name="logo-clear"')

    def test_staff_can_create_recommendation(self):
        user = self._create_staff_user()
        self.client.force_login(user)

        response = self.client.post(
            reverse("homepage:recommendation_create"),
            {
                "name": "Owner Pick",
                "description": "Shown from owner controls.",
                "price": "15.00",
                "is_available": "on",
                "order": "1",
            },
        )

        self.assertRedirects(response, reverse("homepage:owner_dashboard"))
        self.assertTrue(DailyRecommendation.objects.filter(name="Owner Pick").exists())

    def _create_staff_user(self):
        return get_user_model().objects.create_user(
            username="owner",
            password="password",
            is_staff=True,
        )


class MediaCleanupTests(TestCase):
    def setUp(self):
        cache.clear()
        self.media_root = tempfile.mkdtemp()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_root)
        self.settings_override.enable()

    def tearDown(self):
        cache.clear()
        self.settings_override.disable()
        shutil.rmtree(self.media_root, ignore_errors=True)

    def test_deleting_image_model_removes_uploaded_file(self):
        item = DailyRecommendation.objects.create(
            name="Cleanup Dish",
            price="12.00",
            image=SimpleUploadedFile("cleanup.jpg", b"image-data", content_type="image/jpeg"),
        )
        image_path = item.image.path

        self.assertTrue(os.path.exists(image_path))

        item.delete()

        self.assertFalse(os.path.exists(image_path))

    def test_replacing_image_removes_old_uploaded_file(self):
        photo = RestaurantPhoto.objects.create(
            title="Dining room",
            image=SimpleUploadedFile("old-room.jpg", b"old-image", content_type="image/jpeg"),
        )
        old_image_path = photo.image.path

        photo.image = SimpleUploadedFile("new-room.jpg", b"new-image", content_type="image/jpeg")
        photo.save()

        self.assertFalse(os.path.exists(old_image_path))
        self.assertTrue(os.path.exists(photo.image.path))

    def test_shared_image_is_kept_until_last_reference_is_deleted(self):
        shared_name = "recommendations/shared.jpg"
        shared_path = os.path.join(self.media_root, shared_name)
        os.makedirs(os.path.dirname(shared_path), exist_ok=True)
        with open(shared_path, "wb") as image_file:
            image_file.write(b"shared-image")

        first = DailyRecommendation.objects.create(
            name="First Dish",
            price="12.00",
            image=shared_name,
        )
        second = DailyRecommendation.objects.create(
            name="Second Dish",
            price="13.00",
            image=shared_name,
        )

        first.delete()

        self.assertTrue(os.path.exists(shared_path))

        second.delete()

        self.assertFalse(os.path.exists(shared_path))

    def test_past_event_cover_image_is_cleared_on_homepage_load(self):
        event = Event.objects.create(
            title="Past Party",
            event_date=timezone.localdate() - timedelta(days=1),
            cover_image=SimpleUploadedFile("past-party.jpg", b"image-data", content_type="image/jpeg"),
            is_published=True,
        )
        image_path = event.cover_image.path

        self.assertTrue(os.path.exists(image_path))

        self.client.get(reverse("homepage:home"))
        event.refresh_from_db()

        self.assertEqual(event.cover_image.name, "")
        self.assertFalse(os.path.exists(image_path))

    def test_future_event_cover_image_is_kept_on_homepage_load(self):
        event = Event.objects.create(
            title="Future Party",
            event_date=timezone.localdate() + timedelta(days=1),
            cover_image=SimpleUploadedFile("future-party.jpg", b"image-data", content_type="image/jpeg"),
            is_published=True,
        )
        image_path = event.cover_image.path

        self.client.get(reverse("homepage:home"))
        event.refresh_from_db()

        self.assertTrue(event.cover_image.name)
        self.assertTrue(os.path.exists(image_path))

    def test_past_event_cover_image_cleanup_runs_once_per_day(self):
        first_event = Event.objects.create(
            title="First Past Party",
            event_date=timezone.localdate() - timedelta(days=1),
            cover_image=SimpleUploadedFile("first-past-party.jpg", b"first-image", content_type="image/jpeg"),
            is_published=True,
        )
        first_image_path = first_event.cover_image.path

        self.client.get(reverse("homepage:home"))
        first_event.refresh_from_db()

        self.assertEqual(first_event.cover_image.name, "")
        self.assertFalse(os.path.exists(first_image_path))

        second_event = Event.objects.create(
            title="Second Past Party",
            event_date=timezone.localdate() - timedelta(days=1),
            cover_image=SimpleUploadedFile("second-past-party.jpg", b"second-image", content_type="image/jpeg"),
            is_published=True,
        )
        second_image_path = second_event.cover_image.path

        self.client.get(reverse("homepage:home"))
        second_event.refresh_from_db()

        self.assertTrue(second_event.cover_image.name)
        self.assertTrue(os.path.exists(second_image_path))
