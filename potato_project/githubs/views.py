import requests
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Github as GithubModel
from django.utils import timezone


# githubs api를 불러오는 함수
class GitHubAPIService:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_commits(self, repo):
        github_api_url = f"https://api.github.com/repos/{repo}/commits"
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get(github_api_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None, response.status_code


# 데이터베이스에 커밋과 날짜를 저장하는 함수
class GitHubDatabaseService:
    @staticmethod
    def update_or_create_commit_record(user, commit_count, latest_commit_date):
        GithubModel.objects.update_or_create(
            user=user,
            defaults={
                "commit_num": commit_count,
                "date": timezone.now(),
            },
        )
        return {
            "commit_count": commit_count,
            "latest_commit_date": (
                latest_commit_date.isoformat() if latest_commit_date else None
            ),
        }


# Github api를 호출하고 db에 업데이트 하는 함수
class GithubCommitsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.github_access_token:
            return Response({"error": "사용자 권한이 없습니다."}, status=400)

        repo = request.GET.get("repo")
        if not repo:
            return Response(
                {"error": "커밋을 위한 레포지토리가 존재하지 않습니다."}, status=400
            )

        github_service = GitHubAPIService(user.github_access_token)
        commits, status_code = github_service.get_commits(repo)

        if commits is not None:
            commit_count = len(commits)
            latest_commit_date = (
                commits[0]["commit"]["author"]["date"] if commits else None
            )

            db_service = GitHubDatabaseService()
            result = db_service.update_or_create_commit_record(
                user, commit_count, latest_commit_date
            )

            return JsonResponse(result, safe=False)
        else:
            return Response({"error": "커밋 요청을 실패했습니다."}, status=status_code)
