# github/views.py
from django.http import JsonResponse
from github import Github
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from cryptography.fernet import Fernet
from django.conf import settings

# 비밀 키 설정 (서버와 클라이언트 모두에서 동일한 비밀 키 사용) settings 80줄
SECRET_KEY = settings.FERNET_KEY

#encrypted값을 복호화하는 함수
def decrypt_cookie(encrypted_value):
    fernet = Fernet(SECRET_KEY)
    decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()
    return decrypted_value

# 클래스의 모든 메서드가 로그인 사용자만 접근할 수 있도록 하는 데코레이터#
@method_decorator(login_required, name='dispatch')
#view클래스를 상속하여 장고의클래스 기반 뷰를 구현한것
class GetCommitDataView(View):
    def get(self, request, userid):
        #github_access_token의 값을 가져온다
        encrypted_token = request.COOKIES.get('github_access_token')
        if not encrypted_token:
            return JsonResponse({'error': 'GitHub token not found in cookies'}, status=404)

        try: #암호화된 토큰을 복호화해서 github토큰을 얻음 
            token = decrypt_cookie(encrypted_token)
        except Exception as e:
            return JsonResponse({'error': 'Invalid token'}, status=400)

        #pygithub를 사용하여 github token api클라이언트를 생성
        g = Github(token)
        github_user = g.get_user()
        commit_data = []

        # 모든 공개 레포지토리에서 커밋 수와 날짜를 가져옵니다.
        for repo in github_user.get_repos():
            if not repo.private:
                commits = repo.get_commits()
                for commit in commits:
                    commit_data.append({
                        'commit_date': commit.commit.author.date
                    })

        # 커밋 수를 계산하고 커밋 날짜의 최신 날짜를 포함하여 반환합니다.
        commit_count = len(commit_data)
        latest_commit_date = max(commit['commit_date'] for commit in commit_data) if commit_data else None

        result = {
            'commit_count': commit_count,
            'latest_commit_date': latest_commit_date.isoformat() if latest_commit_date else None
        }

        return JsonResponse(result, safe=False)
