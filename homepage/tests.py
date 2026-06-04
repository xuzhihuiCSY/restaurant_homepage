from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import DailyRecommendation


class HomePageTests(TestCase):
    def test_homepage_renders_successfully(self):
        response = self.client.get(reverse("homepage:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurant Name")
        self.assertContains(response, "Chef recommended dishes")

    def test_today_recommendation_renders_on_homepage(self):
        DailyRecommendation.objects.create(
            name="Lunch Special",
            price="12.50",
            display_date=timezone.localdate(),
        )

        response = self.client.get(reverse("homepage:home"))

        self.assertContains(response, "Lunch Special")


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
