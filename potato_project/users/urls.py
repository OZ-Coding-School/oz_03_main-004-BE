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
]
