import unittest
from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from stacks.models import Stack
from stacks.serializers import StackSerializer
from users.models import User


class StackListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="kingtato", nickname="kingtato")
        self.client.force_authenticate(user=self.user)

        self.stack1 = Stack.objects.create(name="Python")
        self.stack2 = Stack.objects.create(name="Java")

        self.url = "/stacks/all"

    def test_get_stack_list_success(self):
        response = self.client.get(self.url)

        # 응답 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터 확인
        response_data = response.json()
        expected_data = StackSerializer([self.stack1, self.stack2], many=True).data
        self.assertEqual(response_data, expected_data)

    def test_get_stack_list_database_error(self):
        with patch("stacks.views.Stack.objects.all", side_effect=DatabaseError):
            response = self.client.get(self.url)

            # 응답 코드 확인
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            # 응답 데이터 확인
            response_data = response.json()
            self.assertEqual(response_data["error"], "DB 에러 발생")

    def test_get_stack_list_serializer_error(self):
        with patch(
            "stacks.views.StackSerializer",
            side_effect=ValidationError("Serializer 에러 발생"),
        ):
            response = self.client.get(self.url)

            # 응답 코드 확인
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # 응답 데이터 확인
            response_data = response.json()
            self.assertEqual(response_data["error"], "Serializer 에러 발생")

    def test_get_stack_list_object_does_not_exist(self):
        with patch("stacks.views.Stack.objects.all", side_effect=ObjectDoesNotExist):
            response = self.client.get(self.url)

            # 응답 코드 확인
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

            # 응답 데이터 확인
            response_data = response.json()
            self.assertEqual(response_data["error"], "object가 존재하지 않습니다")


if __name__ == "__main__":
    unittest.main()
