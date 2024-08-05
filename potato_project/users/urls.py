from django.urls import path
from users import views

urlpatterns = [
    path("accounts/github/login/", views.github_login, name="github_login"),
    path("accounts/github/callback/", views.github_callback, name="github_callback"),
    path(
        "accounts/github/login/finish/",
        views.GithubLogin.as_view(),
        name="github_login_todjango",
    ),
    path(
        "accounts/token/refresh/",
        views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/accounts/logout/", views.logout_view, name="logout"),
    path("api/accounts/profile/", views.UserDetail.as_view(), name="user_detail"),
    path(
        "api/accounts/baekjoon_id/",
        views.UpdateBaekjoonIDView.as_view(),
        name="update-baekjoon-id",
    ),
    path(
        "api/accounts/nickname/",
        views.UserNicknameUpdateView.as_view(),
        name="update-nickname",
    ),
]
