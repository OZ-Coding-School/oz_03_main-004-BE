from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

class GitHubCommitsTests(TestCase):
    def setUp(self):
        # 테스트에 사용할 기본 사용자 생성
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            nickname='testuser',
        )
        self.client.force_authenticate(user=self.user)

    def test_commits_endpoint(self):
        # GitHub 커밋 엔드포인트를 테스트합니다.
        url = reverse('github_commits', kwargs={'userid': 'testuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 응답 데이터 검증을 추가할 수 있습니다.
