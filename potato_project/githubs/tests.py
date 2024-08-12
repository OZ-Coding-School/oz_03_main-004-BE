import unittest
from datetime import date, timedelta
from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

from .views import GitHubAPIService, GitHubDatabaseService


class TestGitHubAPIService(unittest.TestCase):
    def setUp(self):
        self.access_token = "fake_access_token"
        self.github_service = GitHubAPIService(
            self.access_token
        )  # 생성자가 있는 경우에 인자 값 전달 가능
        self.repo = "kingtato/HelloFlower"
        self.username = "kingtato"

    # @patch 문법은 unittest.mock 모듈에서 지원하는 문법이고
    # mock_response로 모의 request 객체를 생성한다.
    # 커밋을 얻어오는 지 테스트한다.
    @patch("githubs.views.requests.get")
    def test_get_commits(self, mock_get):  # 데코레이터로 생성한 Mock 객체를 mock_get
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{"commit": "data"}]

        # 실행
        commits = self.github_service.get_commits(self.repo)

        # 검증
        self.assertEqual(commits, [{"commit": "data"}])
        mock_get.assert_called_once_with(
            f"https://api.github.com/repos/{self.repo}/commits",
            headers={
                "Authorization": f"token {self.access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )

    @patch("githubs.views.requests.get")
    def test_get_repos(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{"repo": "data"}]

        # 실행
        repos = self.github_service.get_repos(self.username)

        # 검증
        self.assertEqual(repos, [{"repo": "data"}])
        mock_get.assert_called_once_with(
            f"https://api.github.com/users/{self.username}/repos",
            headers={
                "Authorization": f"token {self.access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )

    @patch("githubs.views.requests.get")
    def test_get_total_commits(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"total_count": 42}

        # 실행
        total_commits = self.github_service.get_total_commits(self.username)

        # 검증
        self.assertEqual(total_commits, 42)
        mock_get.assert_called_once_with(
            f"https://api.github.com/search/commits?q=author:{self.username}",
            headers={
                "Authorization": f"token {self.access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )

    @patch("githubs.views.requests.get")
    def test_get_commits_error(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # 실행
        commits, status_code = self.github_service.get_commits(self.repo)

        # 검증
        self.assertIsNone(commits)
        self.assertEqual(status_code, 404)

    @patch("githubs.views.requests.get")
    def test_get_repos_error(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # 실행
        repos, status_code = self.github_service.get_repos(self.username)

        # 검증
        self.assertIsNone(repos)
        self.assertEqual(status_code, 404)

    @patch("githubs.views.requests.get")
    def test_get_total_commits_error(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # 실행
        total_commits, status_code = self.github_service.get_total_commits(
            self.username
        )

        # 검증
        self.assertIsNone(total_commits)
        self.assertEqual(status_code, 404)


# 데이터베이스에 커밋과 날짜가 저장되는 지 확인하는 함수
class TestGitHubDataBaseService(TestCase):
    @patch("githubs.models.Github.objects.update_or_create")
    def test_update_or_create_commit_record(self, mock_update_or_create):
        # 테스트 데이터 설정
        user = User.objects.create(username="kingtato")
        commit_count = 5
        commit_date = date(2089, 12, 23)

        # 서비스 메서드 호출
        GitHubDatabaseService.update_or_create_commit_record(
            user, commit_count, commit_date
        )

        # 검증
        mock_update_or_create.assert_called_once_with(
            user=user, date=commit_date, defaults={"commit_num": commit_count}
        )


class GithubCommitsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user.github_access_token = "fake_access_token"
        self.user.save()
        self.client.force_authenticate(user=self.user)

    @patch("gihubs.views.GitHubAPIService.get_repos")
    @patch("gihubs.views.GitHubAPIService.get_commits")
    @patch("gihubs.views.GitHubAPIService.get_total_commits")
    @patch("gihubs.views.GitHubDatabaseService.update_or_create_commit_record")
    def test_get_commits(
        self,
        mock_update_or_create,
        mock_get_total_commits,
        mock_get_commits,
        mock_get_repos,
    ):
        # Mock get_repos response
        mock_get_repos.return_value = ([{"full_name": "test/repo"}], 200)

        # Mock get_commits response
        mock_commit = {
            "commit": {
                "author": {
                    "date": (timezone.now() - timedelta(days=1)).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    )
                }
            }
        }
        mock_get_commits.return_value = ([mock_commit], 200)

        # Mock get_total_commits response
        mock_get_total_commits.return_value = 42

        # Make the request
        response = self.client.get(reverse("github_commits"))

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        response_data = response.json()
        self.assertEqual(response_data["today_commit_count"], 0)
        self.assertEqual(response_data["week_commit_count"], 1)
        self.assertEqual(response_data["total_commit_count"], 42)
        self.assertEqual(response_data["week_average_commit_count"], round(1 / 7, 2))

        # Check that the update_or_create_commit_record was called correctly
        mock_update_or_create.assert_called_once_with(
            self.user, 0, timezone.now().date()
        )

    @patch("gihubs.views.GitHubAPIService.get_repos")
    def test_get_commits_no_token(self, mock_get_repos):
        # Remove the access token
        self.user.github_access_token = ""
        self.user.save()

        # Make the request
        response = self.client.get(reverse("github_commits"))

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"error": "깃허브 액세스 토큰이 없습니다."})

    @patch("gihubs.views.GitHubAPIService.get_repos")
    def test_get_commits_failed_repos_request(self, mock_get_repos):
        # Mock get_repos to return an error
        mock_get_repos.return_value = (None, 404)

        # Make the request
        response = self.client.get(reverse("github_commits"))

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"error": "커밋 요청을 실패했습니다."})


if __name__ == "__main__":
    unittest.main()
