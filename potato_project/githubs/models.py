# github/models.py
from django.db import models
from common.models import TimeStampedModel
from users.models import User


class UserProfile(models.Model):
    # null = True로 한상태에서 데이터베이스 user필드를 업데이트하고 이후에 필드를 null=False로 바꿔야한다
    # 기본값이 있어야 마이그레이션이 되는데 defalut=1로 임시방편 할 수있지만 무결성에 흠이간다고 위에 방법을 추천해주는데 잘 이해못함.
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True
    )
    github_access_token = models.CharField(max_length=255)

    def __str__(self):
        # GitHub의 nickname을 반환
        return self.user.username


class Github(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="github_repositories"
    )
    github_id = models.CharField(max_length=50, unique=True, verbose_name="GitHub ID")
    commit_num = models.BigIntegerField(verbose_name="Commit Number")

    def __str__(self):
        return self.github_id  # GitHub ID를 반환
