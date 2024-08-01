from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse
from potato_types.models import PotatoType
from potato_types.serializers import PotatoTypeSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from users.models import User


class PotatoesListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("potatoes-list")

        # 테스트용 감자 데이터 생성
        self.potato1 = PotatoType.objects.create(
            potato_name="Potato A", potato_description="Description A"
        )
        self.potato2 = PotatoType.objects.create(
            potato_name="Potato B", potato_description="Description B"
        )

    def test_get_potatoes_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        potatoes = PotatoType.objects.all()
        serializer = PotatoTypeSerializer(potatoes, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_get_potatoes_list_database_error(self):
        with patch("potato_types.views.PotatoType.objects.all") as mock_all:
            mock_all.side_effect = DatabaseError("DB 에러 발생")
            response = self.client.get(self.url)
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(response.data["error"], "DB 에러 발생")

    def test_get_potatoes_list_validation_error(self):
        with patch("potato_types.views.PotatoTypeSerializer") as mock_serializer:
            mock_serializer.side_effect = ValidationError("Serializer 에러 발생")
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("Serializer 에러 발생", str(response.data))

    def test_get_potatoes_list_object_does_not_exist(self):
        with patch("potato_types.views.PotatoType.objects.all") as mock_all:
            mock_all.side_effect = ObjectDoesNotExist("object가 존재하지 않습니다")
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data["error"], "object가 존재하지 않습니다")

    def test_get_potatoes_list_general_exception(self):
        with patch("potato_types.views.PotatoType.objects.all") as mock_all:
            mock_all.side_effect = Exception("예기치 않은 오류가 발생했습니다")
            response = self.client.get(self.url)
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(response.data["error"], "예기치 않은 오류가 발생했습니다")
