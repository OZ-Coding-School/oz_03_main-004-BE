from django.db import models
from django.conf import settings  
from common.models import TimeStampedModel 

class Potato(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    potato_type_id = models.SmallIntegerField()  # 감자 타입을 smallint로 직접 저장
    potato_nickname = models.CharField(max_length=20, blank=True, null=True)
    potato_level = models.SmallIntegerField(blank=True, null=True)
    potato_exp = models.SmallIntegerField(blank=True, null=True)
    potato_coin = models.SmallIntegerField(blank=True, null=True)
    is_selected = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.potato_nickname or "Unnamed Potato"
