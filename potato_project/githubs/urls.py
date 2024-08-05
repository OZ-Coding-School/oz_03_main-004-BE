from django.urls import path

from . import views

urlpatterns = [
    path("", views.GithubCommitsView.as_view(), name="github_commits"),
]
