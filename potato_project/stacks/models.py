from django.db import models


class Stack(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="스택명")

    def __str__(self):
        return self.name
