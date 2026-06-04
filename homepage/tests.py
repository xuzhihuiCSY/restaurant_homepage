from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_homepage_renders_successfully(self):
        response = self.client.get(reverse("homepage:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurant Name")
        self.assertContains(response, "Chef recommended dishes")
