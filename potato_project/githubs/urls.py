from django.urls import path
from .views import GithubCommitsView

urlpatterns = [
    path("commits/", GithubCommitsView.as_view(), name="get_commit_data"),
]
