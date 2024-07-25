from django.urls import path
from .views import GithubCommitsView

urlpatterns = [
    path('githubs/commits/', GithubCommitsView(), name='get_commit_data'),
]
