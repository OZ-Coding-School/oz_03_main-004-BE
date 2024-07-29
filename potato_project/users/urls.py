from django.urls import path
from users import views

urlpatterns = [
    path("github/login/", views.github_login, name="github_login"),
    path("github/callback/", views.github_callback, name="github_callback"),
    path(
        "github/login/finish/",
        views.GithubLogin.as_view(),
        name="github_login_todjango",
    ),
    path(
        "token/refresh/", views.CustomTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("profile/", views.UserDetail.as_view(), name="user_detail"),
    path(
        "update-baekjoon-id/",
        views.UpdateBaekjoonIDView.as_view(),
        name="update-baekjoon-id",
    ),
]
