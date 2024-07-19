from django.db import models
from common.models import TimeStampedModel
from users.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_access_token = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Github(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    github_id = models.CharField(max_length=50, verbose_name="깃허브 아이디")
    commit_num = models.BigIntegerField(verbose_name="커밋숫자")

    def __str__(self):
        return self.github_id
