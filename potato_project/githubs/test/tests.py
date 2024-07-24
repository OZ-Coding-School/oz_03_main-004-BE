from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock
from users.models import User

class GetCommitDataViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            nickname="testnickname",
        )
        self.client.login(email="testuser@example.com", password="testpassword")
        
        self.secret_key = "my_secret_key"
        self.token = "mock_github_token"

    @patch("github.views.decrypt_cookie")
    @patch("github.views.Github")
    def test_get_commit_data_success(self, mock_github, mock_decrypt_cookie):
        mock_decrypt_cookie.return_value = self.token
        
        mock_repo = Mock()
        mock_repo.private = False
        mock_commit = Mock()
        mock_commit.commit.author.date = "2024-07-19T12:00:00Z"
        mock_repo.get_commits.return_value = [mock_commit]
        mock_github.return_value.get_user.return_value.get_repos.return_value = [mock_repo]

        url = reverse("get_commit_data")
        response = self.client.get(url, HTTP_COOKIE="github_access_token=encrypted_token")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"commit_count": 1, "latest_commit_date": "2024-07-19T12:00:00"},
        )

    def test_get_commit_data_token_not_found(self):
        self.client.logout()
        url = reverse("get_commit_data")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content, {"error": "GitHub token not found in cookies"}
        )

    def test_get_commit_data_invalid_token(self):
        with patch("github.views.decrypt_cookie", side_effect=Exception("Invalid token")):
            url = reverse("get_commit_data")
            response = self.client.get(url, HTTP_COOKIE="github_access_token=encrypted_token")

            self.assertEqual(response.status_code, 400)
            self.assertJSONEqual(response.content, {"error": "Invalid token"})
