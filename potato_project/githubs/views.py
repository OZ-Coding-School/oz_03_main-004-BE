from datetime import datetime, timedelta

import pytz
import requests
from django.db.models import Avg, Sum
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Github as GithubModel


class GitHubAPIService:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_commits(self, repo, author):
        github_api_url = f"https://api.github.com/repos/{repo}/commits"
        params = {
            "author": author,  # author 파라미터 설정
            "per_page": 100,
        }
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get(github_api_url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json(), 200
        else:
            return None, response.status_code

    def get_repos(self, username):
        github_api_url = f"https://api.github.com/users/{username}/repos"
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get(github_api_url, headers=headers)

        if response.status_code == 200:
            return response.json(), 200
        else:
            return None, response.status_code


# 데이터베이스에 커밋과 날짜를 저장하는 함수
class GitHubDatabaseService:
    @staticmethod
    def update_or_create_commit_record(user, commit_count, date):
        GithubModel.objects.update_or_create(
            user=user,
            date=date,
            defaults={"commit_num": commit_count},
        )


# 깃허브 커밋 조회 및 저장 뷰
class GithubCommitsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.github_access_token:
            return Response({"error": "깃허브 액세스 토큰이 없습니다."}, status=401)

        github_service = GitHubAPIService(user.github_access_token)
        db_service = GitHubDatabaseService()

        # 오늘 날짜
        today = timezone.localtime(timezone.now()).date()

        print("today: ", today)
        # 7일 전 날짜
        week_ago = today - timedelta(days=7)

        # 레포지토리 목록 조회
        repos, status_code = github_service.get_repos(user.username)

        if repos is not None:
            # 오늘, 7일간 커밋 수 계산
            today_commits = 0

            for repo in repos:
                commits, _ = github_service.get_commits(
                    repo["full_name"], user.username
                )
                if commits is not None:
                    for commit in commits:
                        commit_date = (
                            timezone.make_aware(
                                datetime.strptime(
                                    commit["commit"]["author"]["date"],
                                    "%Y-%m-%dT%H:%M:%SZ",
                                ),
                                timezone=pytz.UTC,
                            )
                            .astimezone(timezone.get_current_timezone())
                            .date()
                        )
                        if commit_date == today:
                            today_commits += 1

            # 오늘 커밋 수 데이터베이스에 저장
            db_service = GitHubDatabaseService()
            db_service.update_or_create_commit_record(user, today_commits, today)

            # 최근 7일간 커밋 수 및 전체 커밋 수 계산
            week_commits = (
                GithubModel.objects.filter(user=user, date__gte=week_ago).aggregate(
                    Sum("commit_num")
                )["commit_num__sum"]
                or 0
            )
            total_commits = (
                GithubModel.objects.filter(user=user).aggregate(Sum("commit_num"))[
                    "commit_num__sum"
                ]
                or 0
            )

            # 7일 평균 커밋 수 계산
            week_average_commit_count = round(week_commits / 7, 2)

            # 경험치 및 레벨 업데이트
            user.potato_exp = total_commits
            user.potato_level = 1
            level_up_threshold = int(50 * 1.5 ** (user.potato_level - 1))
            while user.potato_exp >= level_up_threshold:
                user.potato_level += 1
                user.potato_exp -= level_up_threshold
                level_up_threshold = int(50 * 1.5 ** (user.potato_level - 1))
            user.save()

            # 다음 레벨까지 필요한 경험치 계산
            next_level_exp = int(50 * 1.5 ** (user.potato_level - 1)) - user.potato_exp

            # 응답 데이터 생성
            commit_statistics = {
                "today_commit_count": today_commits,
                "week_commit_count": week_commits,
                "total_commit_count": total_commits,
                "week_average_commit_count": week_average_commit_count,
                "level": user.potato_level,
                "exp": user.potato_exp,
                "next_level_exp": int(
                    next_level_exp
                ),  # 다음 레벨까지 필요한 경험치 추가
            }

            return JsonResponse(commit_statistics, safe=False)
        else:
            return Response({"error": "커밋 요청을 실패했습니다."}, status=status_code)
