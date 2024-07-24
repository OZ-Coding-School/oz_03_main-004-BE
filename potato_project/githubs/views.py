import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from github import Github
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Github as GithubModel
from django.utils import timezone

@method_decorator(login_required, name="dispatch")
class GetCommitDataView(View):
    def get(self, request):
        # User 객체를 통해 GitHub 액세스 토큰 가져오기
        user = request.user
        if not user.github_access_token:
            return JsonResponse(
                {"error": "프로필에서 github token을 찾을수없습니다."}, status=404
            )

        try:
            token = user.github_access_token
        except Exception as e:
            return JsonResponse({"error": "토큰을 이용할 수 없습니다."}, status=400)

        # pygithub를 사용하여 github token api 클라이언트를 생성
        g = Github(token)
        github_user = g.get_user()
        commit_data = []

        # 모든 공개 레포지토리에서 커밋 수와 날짜를 가져옵니다./ 레포지토리가 있어야 커밋을 알수있음.
        for repo in github_user.get_repos():
            if not repo.private:
                commits = repo.get_commits()
                for commit in commits:
                    commit_data.append({"commit_date": commit.commit.author.date})

        commit_count = len(commit_data)
        latest_commit_date = (
            max(commit["commit_date"] for commit in commit_data)
            if commit_data
            else None
        )

        # 기존 레코드를 업데이트하거나 새 레코드를 생성/ 유저가 없으면 새롭게 생성함
        GithubModel.objects.update_or_create(
            user=user,
            defaults={
                "commit_num": commit_count,
                "date": timezone.now(),
            }
        )

        result = {
            "commit_count": commit_count,
            "latest_commit_date": (
                latest_commit_date.isoformat() if latest_commit_date else None
            ),
        }

        return JsonResponse(result, safe=False)

#커밋 정보에 다가가기 위해서는 사용자가 인증되있어야하는 코드 
class GithubCommitsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.github_access_token:
            return Response({"error": "사용자 권한이 없습니다."}, status=400)

        repo = request.GET.get("repo")
        if not repo:
            return Response({"error": "커밋을 위한 레포지토리가 존재하지 않습니다."}, status=400)

        github_api_url = f"https://api.github.com/repos/{repo}/commits"
        headers = {
            "Authorization": f"token {user.github_access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get(github_api_url, headers=headers)

        if response.status_code == 200:
            commits = response.json()
            return Response(commits)
        else:
            return Response(
                {"error": "커밋 요청을 실패했습니다."}, status=response.status_code
            )
