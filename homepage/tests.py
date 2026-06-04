from datetime import date

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import CustomerReview, DailyRecommendation, Event, RestaurantProfile


class HomePageTests(TestCase):
    def test_homepage_renders_successfully(self):
        response = self.client.get(reverse("homepage:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurant Name")
        self.assertContains(response, "Restaurant photos")
        self.assertContains(response, "Chef recommended dishes")
        self.assertContains(response, "What guests say")

    def test_today_recommendation_renders_on_homepage(self):
        DailyRecommendation.objects.create(
            name="Lunch Special",
            price="12.50",
            display_date=timezone.localdate(),
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "Lunch Special")

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

    def test_online_order_section_renders_when_visible_with_url(self):
        RestaurantProfile.objects.create(
            name="Test Restaurant",
            show_online_order=True,
            online_order_url="https://order.example.com/menu",
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "Order Online")
        self.assertContains(response, 'href="https://order.example.com/menu"')

    def test_online_order_url_required_when_section_visible(self):
        profile = RestaurantProfile(name="Test Restaurant", show_online_order=True)

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

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Homepage display controls")
        self.assertContains(response, "Restaurant photo display")
        self.assertContains(response, "Review highlights")

    def test_staff_can_create_today_recommendation(self):
        user = self._create_staff_user()
        self.client.force_login(user)

        response = self.client.post(
            reverse("homepage:recommendation_create"),
            {
                "name": "Owner Pick",
                "description": "Shown from owner controls.",
                "price": "15.00",
                "display_date": timezone.localdate().isoformat(),
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
