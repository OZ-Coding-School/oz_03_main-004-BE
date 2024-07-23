# githubs/test/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from users.models import User  # 커스터마이즈된 User 모델 임포트


class GetCommitDataViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # email과 password를 사용하여 사용자 생성
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            nickname="testnickname",
        )
        self.client.login(email="testuser@example.com", password="testpassword")

        self.secret_key = "my_secret_key"

    @patch("github.views.decrypt_cookie")
    @patch("github.views.Github")
    def test_get_commit_data_success(self, mock_github, mock_decrypt_cookie):
        mock_decrypt_cookie.return_value = "mock_token"
        mock_github.return_value.get_user.return_value.get_repos.return_value = [
            mock_repo
        ]

        mock_repo = mock.Mock()
        mock_repo.private = False
        mock_repo.get_commits.return_value = [mock_commit]

        mock_commit = mock.Mock()
        mock_commit.commit.author.date = "2024-07-19T12:00:00Z"

        url = reverse("get_commit_data", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"commit_count": 1, "latest_commit_date": "2024-07-19T12:00:00"},
        )

    def test_get_commit_data_token_not_found(self):
        self.client.logout()
        url = reverse("get_commit_data", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content, {"error": "GitHub token not found in cookies"}
        )

    def test_get_commit_data_invalid_token(self):
        with patch(
            "github.views.decrypt_cookie", side_effect=Exception("Invalid token")
        ):
            url = reverse("get_commit_data", args=[1])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 400)
            self.assertJSONEqual(response.content, {"error": "Invalid token"})
