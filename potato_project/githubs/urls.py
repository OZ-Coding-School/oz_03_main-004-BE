# github/urls.py
from django.urls import path

from .views import GetCommitDataView, GithubCommitsView

urlpatterns = [
    path(
        "<str:userid>/commits/",  # githubs/를 제외
        GetCommitDataView.as_view(),
        name="get_commit_data",
    ),
    path("api/commits/", GithubCommitsView.as_view(), name="github-commits"),
]
