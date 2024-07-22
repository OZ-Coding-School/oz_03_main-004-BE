# github/models.py
from django.db import models
from common.models import TimeStampedModel
from users.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    github_access_token = models.CharField(max_length=255)

    def __str__(self):
        # GitHub의 nickname을 반환, 우선 nickname으로 해둠
        return self.user.nickname  

class Github(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='github_repositories')
    github_id = models.CharField(max_length=50, unique=True, verbose_name="GitHub ID")
    commit_num = models.BigIntegerField(verbose_name="Commit Number")

    def __str__(self):
        return self.github_id  # GitHub ID를 반환
