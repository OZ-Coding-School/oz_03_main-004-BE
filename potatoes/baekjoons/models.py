from django.db import models
from common.models import TimeStampedModel
from django.contrib.auth.models import User

class Baekjoon(TimeStampedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="유저아이디")
    score = models.BigIntegerField(verbose_name="백준 점수")

    def __str__(self):
        return f"{self.user_id.username} - {self.score}"
