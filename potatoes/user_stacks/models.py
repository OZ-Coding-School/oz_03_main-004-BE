from django.db import models
from django.conf import settings  # 예시로 Django 기본 유저 모델 사용

class UserStack(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="유저아이디")
    stack_id = models.BigIntegerField(verbose_name="스택아이디")

    def __str__(self):
        return f"{self.user_id.username} - {self.stack_id}"
