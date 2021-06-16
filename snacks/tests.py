# from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse
from .models import Snack
from django.contrib.auth import get_user_model

# Create your tests here.
class TestingPages(TestCase):
    
    def test_home_response_status_ok(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tala", email="talahajeer@gmail.com", password="blabla"
        )
        self.snack = Snack.objects.create(
            name="KitKat", purchaser=self.user, description='Red cover chocolate',
        )


    def test_string_representation(self):
        self.assertEqual(str(self.snack), "KitKat")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.name}", "KitKat")
        self.assertEqual(f"{self.snack.purchaser}", "tala")
        self.assertEqual(self.snack.description, "Red cover chocolate")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "KitKat")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/1000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {"name":"Shawerma",
             "description":'Sandwich',
             "purchaser": 'tala',
            }, follow=True
        )
        self.assertContains(response, "Sandwich")