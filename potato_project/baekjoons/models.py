from common.models import TimeStampedModel
from django.db import models
from users.models import User


class Baekjoon(TimeStampedModel):
    # 이거도 _id 빼보겠음
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="유저아이디")
    username = models.CharField(max_length=255, verbose_name="백준 아이디")
    score = models.BigIntegerField(verbose_name="백준 점수")

    def __str__(self):
        return f"{self.user_id.username} - {self.score}"
