from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일자")

    class Meta:
        abstract = True
