import unittest
from unittest.mock import patch

from .views import GitHubAPIService


class TestGitHubAPIService(unittest.TestCase):
    def setUp(self):
        self.access_token = 'fake_access_token'
        self.github_service = GitHubAPIService(self.access_token) # 생성자가 있는 경우에 인자 값 전달 가능
        self.repo = 'kingtato/HelloFlower'
        self.username = 'kingtato'
    
    # @patch 문법은 unittest.mock 모듈에서 지원하는 문법
    # request.get을 모킹한다.
    # 커밋을 얻어오는 지 테스트한다.
    @patch('githubs.views.requests.get')
    def test_get_commits(self, mock_get): # 데코레이터로 생성한 Mock 객체를 mock_get 
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
            }
        )

    @patch('githubs.views.requests.get')
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
            }
        )

    @patch('githubs.views.requests.get')
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
            }
        )

    @patch('githubs.views.requests.get')
    def test_get_commits_error(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # 실행
        commits, status_code = self.github_service.get_commits(self.repo)

        # 검증
        self.assertIsNone(commits)
        self.assertEqual(status_code, 404)

    @patch('githubs.views.requests.get')
    def test_get_repos_error(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # 실행
        repos, status_code = self.github_service.get_repos(self.username)

        # 검증
        self.assertIsNone(repos)
        self.assertEqual(status_code, 404)

    @patch('githubs.views.requests.get')
    def test_get_total_commits_error(self, mock_get):
        # 설정
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # 실행
        total_commits, status_code = self.github_service.get_total_commits(self.username)

        # 검증
        self.assertIsNone(total_commits)
        self.assertEqual(status_code, 404)


if __name__ == '__main__':
    unittest.main()
