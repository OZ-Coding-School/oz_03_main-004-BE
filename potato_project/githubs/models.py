# github/models.py
from common.models import TimeStampedModel
from django.db import models
from django.utils import timezone
from users.models import User


class Github(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User_id")
    commit_num = models.BigIntegerField(verbose_name="Commit Number")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.date}-{self.commit_num}"
