from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from users.models import User
from users.views import UserDetail


# 테스트할 url이 존재하지 않아서, RequestFactory로 테스트 생성
class UserDetailTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="password", nickname="testpotato"
        )

    def test_get_user_profile(self):
        request = self.factory.get("/user/profile/")
        force_authenticate(request, user=self.user)
        response = UserDetail.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["nickname"], self.user.nickname)


class UpdateBaekjoonIDViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password", nickname="testpotato"
        )
        self.url = reverse("update-baekjoon-id")

    def test_update_baekjoon_id_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            self.url,
            {"baekjoon_id": "new_baekjoon_id"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.baekjoon_id, "new_baekjoon_id")

    def test_update_baekjoon_id_missing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "백준 아이디를 입력해주세요.")


class UserNicknameUpdateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.url = reverse("update-nickname")

    def test_update_nickname_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            self.url,
            {"nickname": "new_nickname"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, "new_nickname")

    def test_update_nickname_missing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "닉네임을 입력해주세요.")
