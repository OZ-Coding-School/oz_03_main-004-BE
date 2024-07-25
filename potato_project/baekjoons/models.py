from common.models import TimeStampedModel
from django.db import models
from users.models import User


class Baekjoon(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="유저아이디")
    score = models.BigIntegerField(verbose_name="백준 점수")  # 백준 아이디 필드 제거

    def __str__(self):
        return f"{self.user.username} - {self.score}"
