from django.db import models


class PotatoType(models.Model):
    # 추가 필드 정의
    potato_name = models.CharField(max_length=255, verbose_name="감자이름")
    potato_image = models.CharField(max_length=255, verbose_name="감자이미지")
    potato_description = models.TextField(verbose_name="감자설명")

    def __str__(self):
        return self.potato_name
