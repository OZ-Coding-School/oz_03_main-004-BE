from common.models import TimeStampedModel  # TimeStampedModel을 가져오기 위해 사용
from django.db import models
from users.models import User


class Todo(TimeStampedModel):
    # field이름은 _id를 붙이지 않는게 좋다고하네?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    date = models.DateTimeField()

    def __str__(self):
        return self.task
