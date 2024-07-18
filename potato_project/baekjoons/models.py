from django.db import models
from common.models import TimeStampedModel
from django.conf import settings

class Baekjoon(TimeStampedModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="유저아이디")
    score = models.BigIntegerField(verbose_name="백준 점수")

    def __str__(self):
        return f"{self.user_id.username} - {self.score}"
