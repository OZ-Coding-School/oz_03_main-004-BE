from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

from .models import Baekjoon


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", baekjoon_id="test_baekjoon"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("profile-view")

    @patch("baekjoons.views.get_boj_profile")
    def test_get_profile_success(self, mock_get_boj_profile):
        mock_get_boj_profile.return_value = {
            "username": "test_baekjoon",
            "tier": 10,
            "solved_count": 50,
            "rating": 1500,
        }

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "test_baekjoon")
        self.assertEqual(response.json()["solved_count"], 50)

        baekjoon = Baekjoon.objects.get(user=self.user)
        self.assertEqual(baekjoon.score, 50)

    def test_get_profile_no_baekjoon_id(self):
        self.user.baekjoon_id = ""
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "User does not have a Baekjoon ID.")

    @patch("baekjoons.views.get_boj_profile")
    def test_get_profile_user_not_found(self, mock_get_boj_profile):
        mock_get_boj_profile.return_value = None

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["error"], "User not found or API error.")


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", baekjoon_id="test_baekjoon"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("profile-view")

    @patch("baekjoons.views.get_boj_profile")
    def test_get_profile_success(self, mock_get_boj_profile):
        mock_get_boj_profile.return_value = {
            "username": "test_baekjoon",
            "tier": 10,
            "solved_count": 50,
            "rating": 1500,
        }

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], "test_baekjoon")
        self.assertEqual(response.json()["solved_count"], 50)

        baekjoon = Baekjoon.objects.get(user=self.user)
        self.assertEqual(baekjoon.score, 50)

    def test_get_profile_no_baekjoon_id(self):
        self.user.baekjoon_id = ""
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "User does not have a Baekjoon ID.")

    @patch("baekjoons.views.get_boj_profile")
    def test_get_profile_user_not_found(self, mock_get_boj_profile):
        mock_get_boj_profile.return_value = None

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["error"], "User not found or API error.")
