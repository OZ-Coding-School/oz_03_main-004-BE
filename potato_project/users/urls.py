from django.urls import path
from users import views
from .views import UpdateBaekjoonIDView

urlpatterns = [
    path("github/login/", views.github_login, name="github_login"),
    path("github/callback/", views.github_callback, name="github_callback"),
    path(
        "github/login/finish/",
        views.GithubLogin.as_view(),
        name="github_login_todjango",
    ),
    path('update-baekjoon-id/', UpdateBaekjoonIDView.as_view(), name='update_baekjoon_id'),
]
