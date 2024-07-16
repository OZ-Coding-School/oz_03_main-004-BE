from django.db import models
from common.models import TimeStampedModel
from django.conf import settings

class Potato(TimeStampedModel):
    # 추가 필드 정의
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="유저아이디")
    potato_type_id = models.SmallIntegerField(verbose_name="감자타입")
    potato_nickname = models.CharField(max_length=255, verbose_name="감자닉네임")
    potato_level = models.IntegerField(verbose_name="감자레벨")
    potato_exp = models.IntegerField(verbose_name="감자경험치")
    potato_coin = models.IntegerField(verbose_name="감자코인")
    is_selected = models.BooleanField(default=False, verbose_name="현재선택상태")

    def __str__(self):
        return self.potato_nickname
