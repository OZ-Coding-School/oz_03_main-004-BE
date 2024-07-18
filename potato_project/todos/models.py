from django.db import models
from django.conf import settings  # 유저 모델을 가져오기 위해 사용
from common.models import TimeStampedModel  # TimeStampedModel을 가져오기 위해 사용

class Todo(TimeStampedModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    date = models.DateTimeField()

    def __str__(self):
        return self.task