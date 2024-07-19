import os
from json.decoder import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers import github, google
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from dotenv import load_dotenv
from rest_framework import status
from users.models import User

load_dotenv()  # .env 파일 로드


state = os.environ.get("STATE")
BASE_URL = "http://localhost:8000/"
GITHUB_CALLBACK_URI = BASE_URL + "users/github/callback"


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
    error = request.GET.get("error")

    if error:
        return JsonResponse(
            {"error": error, "description": request.GET.get("error_description")},
            status=400,
        )

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    """
    Access Token Request
    """

    token_req = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": GITHUB_CALLBACK_URI,
        },
        headers={"Accept": "application/json"},
    )

    token_req_json = token_req.json()
    print(f"Token request response: {token_req_json}")

    error = token_req_json.get("error")
    if error:
        return JsonResponse(
            {"error": error, "description": token_req_json.get("error_description")},
            status=400,
        )

    access_token = token_req_json.get("access_token")

    """
    Email Request
    """
    user_req = requests.get(
        f"https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_json = user_req.json()
    error = user_json.get("error")
    if error is not None:
        raise ValueError(f"GitHub API error: {error}")
    # print(user_json)
    email = user_json.get("email")

    # 응답받은 Access Token을 로그인된 사용자의 Email을 응답받기 위해 url parameter에 포함하여 요청 - Access Token이 틀렸거나, 에러 발생으로 200 OK 코드를 응답받지 못하면 400으로 Response

    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 github로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)


class GithubLogin(SocialLoginView):
    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client


"""
1. 전달받은 email과 동일한 Email이 있는지 찾아본다.
2-1. 만약 있다면?
       - FK로 연결되어있는 socialaccount 테이블에서 이메일의 유저가 있는지 체크
       - 있으면 로그인 진행, 해당 유저의 JWT 발급, 그러나 도중에          
         예기치 못한 오류가 발생하면 에러 메세지와 함께 오류 Status 응답
2-2. 없다면 (신규 유저이면)
       - 회원가입 진행 및 해당 유저의 JWT 발급
       - 그러나 도중에 예기치 못한 오류가 발생하면 에러 메세지와 함께 오류 Status응답
"""
