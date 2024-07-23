from common.models import TimeStampedModel
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    # 일반 유저 생성 함수
    def create_user(self, username, **extra_fields):
        if not username:
            raise ValueError("The username must be provided")

        user = self.model(username=username, **extra_fields)
        user.save()

        return user

    # 슈퍼 유저 생성 함수
<<<<<<< HEAD
    def create_superuser(self, username, **extra_fields):
        user = self.create_user(username**extra_fields)
=======
    def create_superuser(self, username, password, **extra_fields):  
        user = self.create_user(username, **extra_fields)
>>>>>>> develop

        user.is_superuser = True
        user.is_staff = True

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    # 로그인 관련 필드
    username = models.CharField(max_length=255, null=False, unique=True)

    # 프로필 관련 필드
    profile_url = models.CharField(max_length=255, null=True)
    github_id = models.CharField(max_length=255, null=True)
    baekjoon_id = models.CharField(max_length=255, null=True, default="")

    # 감자 관련 필드
    potato_level = models.PositiveIntegerField(null=False, default=0)
    potato_exp = models.PositiveIntegerField(null=False, default=0)

    # Permissions Mixin : 유저의 권한 관리
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

<<<<<<< HEAD
    objects = (
        UserManager()
    )  # 유저를 생성 및 관리 (유저를 구분해서 관리하기 위해 - 관리자계정, 일반계정)
=======
    objects = UserManager()  # 유저를 생성 및 관리 (유저를 구분해서 관리하기 위해 - 관리자계정, 일반계정)
>>>>>>> develop

    def __str__(self):
        return self.username
