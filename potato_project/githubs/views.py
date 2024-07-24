from django.http import JsonResponse
from github import Github
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from cryptography.fernet import Fernet
from django.conf import settings

# 비밀 키 설정
SECRET_KEY = settings.FERNET_KEY


# encrypted값을 복호화하는 함수
def decrypt_cookie(encrypted_value):
    fernet = Fernet(SECRET_KEY)
    decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()
    return decrypted_value


@method_decorator(login_required, name="dispatch")
class GetCommitDataView(View):
    def get(self, request):
        # github_access_token의 값을 가져온다
        encrypted_token = request.COOKIES.get("github_access_token")
        if not encrypted_token:
            return JsonResponse(
                {"error": "GitHub token not found in cookies"}, status=404
            )

        try:
            token = decrypt_cookie(encrypted_token)
        except Exception as e:
            return JsonResponse({"error": "Invalid token"}, status=400)

        # pygithub를 사용하여 github token api 클라이언트를 생성
        g = Github(token)
        github_user = g.get_user()
        commit_data = []

        # 모든 공개 레포지토리에서 커밋 수와 날짜를 가져옵니다.
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

        result = {
            "commit_count": commit_count,
            "latest_commit_date": (
                latest_commit_date.isoformat() if latest_commit_date else None
            ),
        }

        return JsonResponse(result, safe=False)
