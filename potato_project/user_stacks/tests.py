from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import User

from .models import Stack, UserStack
from .serializers import UserStackSerializer


class UserStackListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", nickname="testpotato")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 스택과 유저 스택 생성
        self.stack1 = Stack.objects.create(name="Django")
        self.stack2 = Stack.objects.create(name="React")
        self.user_stack1 = UserStack.objects.create(user=self.user, stack=self.stack1)
        self.user_stack1 = UserStack.objects.create(user=self.user, stack=self.stack2)

        self.url = reverse("user_stack_list")

    def test_get_user_stacks(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        stacks = UserStack.objects.filter(user=self.user)
        serializer = UserStackSerializer(stacks, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_get_user_stacks_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserStackCreateTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("user_stack_create")

    def test_create_user_stack(self):
        data = {"stack_id": 1}  # 존재하는 stack_id를 사용해야 합니다.
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(UserStack.objects.count(), 1)
        self.assertEqual(UserStack.objects.get().stack_id, 1)

    def test_create_user_stack_missing_stack_id(self):
        data = {}  # stack_id가 없는 경우
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserStack.objects.count(), 0)
        self.assertIn("error", response.data)


class UserStackDeleteTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", nickname="testuser")
        self.client.force_authenticate(user=self.user)
        self.stack = UserStack.objects.create(user=self.user, stack_id=1)
        self.url = reverse(
            "user_stack_delete", kwargs={"user_stack_id": self.stack.stack.id}
        )

    def test_delete_user_stack(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserStack.objects.count(), 0)
        self.assertIn("message", response.data)

    def test_delete_non_existent_user_stack(self):
        non_existent_url = reverse(
            "user_stack_delete", kwargs={"user_stack_id": (self.stack.stack.id + 1)}
        )
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_user_stack_not_owned(self):
        other_user = User.objects.create_user(username="otheruser", nickname="testuser")
        other_stack = UserStack.objects.create(user=other_user, stack_id=2)
        other_stack_url = reverse(
            "user_stack_delete",
            kwargs={"user_stack_id": (other_stack.stack_id + 1)},
        )
        response = self.client.delete(other_stack_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
