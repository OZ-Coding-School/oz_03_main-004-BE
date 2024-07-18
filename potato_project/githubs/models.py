from django.db import models
from common.models import TimeStampedModel

class GithubFolder(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    github_id = models.CharField(max_length=50, verbose_name="깃허브 아이디")
    commit_num = models.BigIntegerField(verbose_name="커밋숫자")


    def __str__(self):
        return self.github_int

