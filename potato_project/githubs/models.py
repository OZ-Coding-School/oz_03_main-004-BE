# github/models.py
from common.models import TimeStampedModel
from django.db import models
from users.models import User


class Github(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User id")
    commit_num = models.BigIntegerField(verbose_name="Commit Number")
    date = date = models.DateTimeField()

    def __str__(self):
        return self.github_id  # GitHub ID를 반환
