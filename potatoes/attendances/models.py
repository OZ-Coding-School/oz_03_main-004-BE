from django.db import models
from django.conf import settings
from common.models import TimeStampedModel

class Attendance(TimeStampedModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="유저아이디")
    date = models.DateField(verbose_name="날짜")
    coin_awarded = models.IntegerField(verbose_name="지급된 코인수")

    def __str__(self):
        return f"{self.user_id.username} - {self.date}"