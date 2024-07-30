import os
from datetime import timedelta
from pathlib import Path

from cryptography.fernet import Fernet
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# Django 비밀 키 및 디버그 설정
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Application definition
DJANGO_SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

CUSTOM_USER_APPS = [
    # my app
    "users.apps.UsersConfig",
    "core",
    "attendances.apps.AttendancesConfig",
    "baekjoons.apps.BaekjoonsConfig",
    "common.apps.CommonConfig",
    "githubs.apps.GithubsConfig",
    "potatoes.apps.PotatoesConfig",
    "potato_types.apps.PotatoTypesConfig",
    "stacks.apps.StacksConfig",
    "user_stacks.apps.UserStacksConfig",
    "todos.apps.TodosConfig",
    # django-rest-framework
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # django-rest-auth
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # django-allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
]

INSTALLED_APPS = DJANGO_SYSTEM_APPS + CUSTOM_USER_APPS

# Custom user model
AUTH_USER_MODEL = "users.User"

# 사이트 ID
SITE_ID = 1

# 인증 백엔드 설정
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# 미들웨어 설정
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# URL 설정
ROOT_URLCONF = "app.urls"

# 템플릿 설정
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI 애플리케이션 설정
WSGI_APPLICATION = "app.wsgi.application"


# 데이터베이스 설정
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

# 비밀번호 검증 설정
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 국제화 설정
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 정적 파일 설정
STATIC_URL = "static/"

# 기본 Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework 설정
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# JWT 및 기타 설정
REST_USE_JWT = True
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),  # 액세스 토큰 만료 시간
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # 리프레시 토큰 만료 시간
    "ROTATE_REFRESH_TOKENS": False,  # 리프레시 토큰 순환 사용 여부
    "BLACKLIST_AFTER_ROTATION": False,  # 순환 사용 시 이전 리프레시 토큰 블랙리스트 등록 여부
    "AUTH_HEADER_TYPES": ("Bearer",),  # 인증 헤더 타입
    "UPDATE_LAST_LOGIN": True,
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "my-app-auth",
    "JWT_AUTH_REFRESH_COOKIE": "my-refresh-token",
}

SOCIAL_AUTH_GITHUB_CLIENT_ID = os.environ.get("SOCIAL_AUTH_GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get("SOCIAL_AUTH_GITHUB_SECRET")
STATE = os.environ.get("STATE")


# SOCIALACCOUNT_PROVIDERS = {
#     "github": {
#         "APP": {
#             "client_id": os.environ.get("SOCIAL_AUTH_GITHUB_CLIENT_ID"),
#             "secret": os.environ.get("SOCIAL_AUTH_GITHUB_SECRET"),
#             "key": "",
#         },
#     },
# }

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "SCOPE": [
            "user",
            "repo",
            "read:org",
        ],
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = "https://d3hcv7ngm54uy8.cloudfront.net/oauth-callback"
ACCOUNT_LOGOUT_REDIRECT_URL = "https://d3hcv7ngm54uy8.cloudfront.net/landing"
