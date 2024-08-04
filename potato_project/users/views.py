import json
import os
from json.decoder import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

# .env 파일에서 환경 변수 로드 (python-dotenv 라이브러리 필요)
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from users.models import User

from .serializers import UserSerializer

load_dotenv()  # .env 파일 로드

state = os.environ.get("STATE")
BASE_URL = "https://api.gitpotatoes.com/"
# BASE_URL = "http://localhost:8000"
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
        return JsonResponse(
            {"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST
        )

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
    user_response.encoding = "utf-8"
    user_json = user_response.json()

    # 에러 처리
    if not user_response.ok:
        return JsonResponse(
            {"error": "Failed to get user info"}, status=status.HTTP_401_UNAUTHORIZED
        )

    print(f"User response: {user_response.json()}")

    # 사용자 생성/업데이트 및 로그인
    username = user_json.get("login")
    if not username:
        # 깃허브 계정에 username 없는 경우
        return JsonResponse({"err_msg": "failed to signup"}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            profile_url=user_json.get("avatar_url"),
            github_id=user_json.get("login"),
            nickname=user_json.get("login"),
        )

    # 프로필 이미지 업데이트
    # 깃허브 액세스토큰 업데이트
    user.profile_url = user_json.get("avatar_url", user.profile_url)
    user.github_access_token = access_token
    user.save()

    try:
        social_account, created = SocialAccount.objects.update_or_create(
            user=user,
            provider="github",
            defaults={
                "uid": str(user_json.get("id")),
                "extra_data": user_json,
            },
        )
    except IntegrityError:
        # 이미 존재하는 계정이라면 그냥 진행
        social_account = SocialAccount.objects.get(user=user, provider="github")

    # 로그인 처리 및 응답
    data = {"access_token": access_token, "code": code}
    login_response = requests.post(
        f"{BASE_URL}accounts/github/login/finish/", data=data
    )

    print(f"Login response status: {login_response.status_code}")
    print(f"Login response content: {login_response.text}")

    if not login_response.ok:
        return JsonResponse(
            {"err_msg": "failed to login"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        login_data = login_response.json()
    except json.JSONDecodeError:
        return JsonResponse(
            {"err_msg": "Invalid response from server"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response = JsonResponse(login_data)
    response.set_cookie(
        "access_token",
        login_data.get("access_token"),
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    response.set_cookie(
        "refresh_token",
        login_data.get("refresh_token"),
        httponly=True,
        secure=True,
        samesite="Lax",
    )

    jwt_access_token = login_data.get("access_token")
    jwt_refresh_token = login_data.get("refresh_token")
    user_data = (
        {
            "pk": user.pk,
            "username": user.username,
            "profile_url": user.profile_url,
            "nickname": user.nickname,
        },
    )
    redirect_url = f"https://www.gitpotatoes.com/oauth-callback?access_token={jwt_access_token}&refresh_token={jwt_refresh_token}&user={json.dumps(user_data)}"
    return redirect(redirect_url)
    # return response


class GithubLogin(SocialLoginView):
    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()
        if isinstance(response, HttpResponse):
            user = self.user
            refresh = RefreshToken.for_user(user)

            try:
                social_account = SocialAccount.objects.get(user=user, provider="github")
            except SocialAccount.DoesNotExist:
                # 소셜 계정이 없는 경우 처리
                return JsonResponse({"error": "Social account not found"}, status=400)

            response_data = {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": {
                    "pk": user.pk,
                    "username": user.username,
                    "profile_url": user.profile_url,
                    "nickname": user.nickname,
                },
            }
            return JsonResponse(response_data)
        return response

    """
    깃허브 소셜로그인만 단독으로 사용할거면
    코드 간소화 가능
    -> SocialAccount 모델을 사용하지 않고 직접 User 모델에 GitHub 정보를 저장하는 방식
    """


# 리프레시토큰으로 새 엑세스토큰 발급
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = RefreshToken(request.data.get("refresh"))
        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        new_access_token = refresh_token.access_token

        if not refresh_token.is_valid("refresh"):  # 리프레시 토큰 만료 검사
            return Response(
                {"error": "Expired refresh token. Please login again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh_token.blacklist()  # 이전 리프레시 토큰 블랙리스트 처리

        new_access_token = str(refresh_token.access_token)
        new_refresh_token = str(RefreshToken.for_user(request.user))

        response = Response(
            {"message": "Token refresh successful"}, status=status.HTTP_200_OK
        )

        # 액세스 토큰을 쿠키에 설정
        response.set_cookie(
            "access_token",
            new_access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        # 리프레시 토큰을 쿠키에 설정
        response.set_cookie(
            "refresh_token",
            new_refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response


# 로그아웃 후 랜딩 페이지로 이동
def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


# 유저 프로필 정보 조회
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            serializer = UserSerializer(user)
            return Response(serializer.data)

        # 데이터베이스 연결 또는 쿼리 오류 처리
        except DatabaseError as e:
            return Response(
                {"error": "DB 에러 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # 시리얼라이저 오류 처리
        except ValidationError as e:
            return Response(
                {"error": "Serializer 에러 발생", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 객체가 존재하지 않을 때의 오류 처리
        except ObjectDoesNotExist as e:
            return Response(
                {"error": "object가 존재하지 않습니다", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        # 기타 일반 예외 처리
        except Exception as e:
            return Response(
                {"error": "예기치 않은 오류가 발생했습니다", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateBaekjoonIDView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        new_baekjoon_id = request.data.get("baekjoon_id")
        if not new_baekjoon_id:
            return Response(
                {"status": "error", "message": "백준 아이디를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 필요하다면 백준 아이디 유효성 검사 로직 추가 (예: 길이, 형식 등)

        request.user.baekjoon_id = new_baekjoon_id
        request.user.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class UserNicknameUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        new_nickname = request.data.get("nickname")
        if not new_nickname:
            return Response(
                {"status": "error", "message": "닉네임을 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 닉네임 unique 설정시
        # if User.objects.filter(nickname=new_nickname).exclude(pk=request.user.pk).exists():
        #     return Response({"status": "error", "message": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.nickname = new_nickname
        request.user.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)
