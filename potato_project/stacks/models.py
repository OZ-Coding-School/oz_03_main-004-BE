from django.db import models

class Stack(models.Model):
    name = models.CharField(max_length=20, null=True, verbose_name="스택명")

    def __str__(self):
        return self.name if self.name else "배워가는 감자에요"