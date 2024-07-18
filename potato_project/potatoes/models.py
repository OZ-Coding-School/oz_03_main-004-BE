from django.db import models
from django.conf import settings  
from common.models import TimeStampedModel 

class Potato(TimeStampedModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    potato_type_id = models.SmallIntegerField()  # 감자 타입을 smallint로 직접 저장
    is_selected = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.potato_nickname or "Unnamed Potato"
