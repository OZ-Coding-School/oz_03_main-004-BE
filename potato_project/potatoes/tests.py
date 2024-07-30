import unittest

from django.test import TestCase
from potato_types.models import PotatoType
from potatoes.models import Potato
from potatoes.serializers import PotatoSerializer
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


class MyPotatoDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="kingtato",
            nickname="kingtato",
            password="testpassword",
            potato_level=1,
            potato_exp=1,
        )
        self.client.force_authenticate(user=self.user)

        self.potato_type1 = PotatoType.objects.create(
            potato_name="Type1", potato_description="Type1 Description"
        )
        self.potato1 = Potato.objects.create(
            user=self.user,
            potato_type=self.potato_type1,
            is_acquired=True,
            is_selected=False,
        )

        self.url = "/potatoes/collection/"

    def test_get_my_potato_success(self):
        response = self.client.get(self.url)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터 확인
        response_data = response.json()
        self.assertTrue(len(response_data) > 0)
        self.assertEqual(response_data[0]["user"], self.user.id)
        self.assertEqual(response_data[0]["potato_type"], self.potato_type1.id)

    def test_get_my_potato_not_found(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 응답 데이터 확인
        response_data = response.json()
        self.assertEqual(
            response_data["detail"], "Authentication credentials were not provided."
        )

    def test_get_my_potato_no_potatoes(self):
        # 감자를 모두 삭제하여 유저가 감자를 가지고 있지 않도록 설정
        Potato.objects.filter(user=self.user).delete()
        response = self.client.get(self.url)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # 응답 데이터 확인
        response_data = response.json()
        self.assertEqual(response_data["error"], "object가 존재하지 않습니다")


if __name__ == "__main__":
    unittest.main()
