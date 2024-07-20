import os
from json.decoder import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status

from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

# .env 파일에서 환경 변수 로드 (python-dotenv 라이브러리 필요)
from dotenv import load_dotenv
load_dotenv()  # .env 파일 로드


state = os.environ.get("STATE")
BASE_URL = "http://localhost:8000/" # 프론트엔드 URL로 변경해야 함
GITHUB_CALLBACK_URI = BASE_URL + "accounts/github/callback/"


def github_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_GITHUB_CLIENT_ID")
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={GITHUB_CALLBACK_URI}&scope=user:email"
    )


# 이 함수와 매핑된 url로 들어가면, client_id, redirect uri 등과 같은 정보를 url parameter로 함께 보내 리다이렉트한다.
# 그러면 깃허브 로그인 창이 뜨고, 알맞은 아이디, 비밀번호로 진행하면 Callback URI로 Code값이 들어가게 된다.


def github_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GITHUB_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GITHUB_SECRET")
    code = request.GET.get("code")
    state = request.GET.get("state")
    error = request.GET.get("error")

    # 에러 처리
    if "error" in request.GET:
        return JsonResponse(
            {
                "error": request.GET.get("error"),
                "description": request.GET.get("error_description"),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not code:
        return JsonResponse({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    print(f"Received code: {code}")
    print(f"Received state: {state}")


    # Access Token 요청
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": GITHUB_CALLBACK_URI,
        },
        headers={"Accept": "application/json"},
    )
    token_json = token_response.json()
    access_token = token_json.get("access_token")
    
    # 에러 처리
    if not token_response.ok:
        return JsonResponse(
            {"error": "Failed to get access token"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
    print(f"Token response: {token_response.json()}")

    # 사용자 정보 요청
    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_json = user_response.json()

    # 에러 처리
    if not user_response.ok:
        return JsonResponse({"error": "Failed to get user info"}, status=status.HTTP_401_UNAUTHORIZED)
    
    print(f"User response: {user_response.json()}")
    
    username = user_json.get("login")
    if not username:
        # 깃허브 계정에 username 없는 경우
        return JsonResponse({"err_msg": "failed to signup"}, status=400)


    # 사용자 생성/업데이트 및 로그인
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=user_json.get("email"),
            profile_url=user_json.get("avatar_url"),
            github_id=user_json.get("login"),
        )
            
    user.profile_url = user_json.get("avatar_url", user.profile_url)  # 프로필 이미지 업데이트
    user.save()

    social_account, _ = SocialAccount.objects.get_or_create(
        user=user,
        provider='github',
        uid=str(user_json.get("id")),
        extra_data=user_json,
    )

    # 로그인 처리 및 응답
    data = {"access_token": access_token, "code": code}
    login_response = requests.post(
        f"{BASE_URL}accounts/github/login/finish/", data=data
    )
    
    # 에러 처리 (Bad Request)
    if not login_response.ok:
        return JsonResponse(
            {"err_msg": "failed to login"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    login_data = login_response.json()
    login_data.pop("user",None) # user 정보 제외

    return JsonResponse(login_data)

class GithubLogin(SocialLoginView):
    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client
    
class CustomLogoutView(LogoutView):
    def logout(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            print(e)
        response = super().logout(request)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


"""
1. 전달받은 username과 동일한 username이 있는지 찾아본다.
2-1. 만약 있다면?
       - 있으면 로그인 진행, 해당 유저의 JWT 발급, 그러나 도중에          
         예기치 못한 오류가 발생하면 에러 메세지와 함께 오류 Status 응답
2-2. 없다면 (신규 유저이면)
       - 회원가입 진행 및 해당 유저의 JWT 발급
       - 그러나 도중에 예기치 못한 오류가 발생하면 에러 메세지와 함께 오류 Status응답
"""
