from common.models import TimeStampedModel  # TimeStampedModel을 가져오기 위해 사용
from django.db import models
from stacks.models import Stack
from users.models import User


class UserStack(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="유저아이디")
    stack = models.ForeignKey(
        Stack, on_delete=models.CASCADE, verbose_name="스택아이디"
    )

    def __str__(self):
        return (
            f"{self.user_id.username} - {self.stack_id}"
            if f"{self.user_id.username} - {self.stack_id}"
            else "배워가는 감자에요"
        )
