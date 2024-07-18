from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from common.models import TimeStampedModel


class UserManager(BaseUserManager):
    # 일반 유저 생성 함수
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please enter an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    # 슈퍼 유저 생성 함수
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    # 로그인 관련 필드
    email = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)

    # 프로필 관련 필드
    name = models.CharField(max_length=20, null=False)
    nickname = models.CharField(max_length=255, null=False, unique=True)
    birthday = models.DateField(blank=True, null=True)
    profile_url = models.CharField(max_length=255, null=True)
    github_id = models.CharField(max_length=255, null=True)
    baekjoon_id = models.CharField(max_length=255, null=True)

    # 감자 관련 필드
    potato_level = models.PositiveIntegerField(null=False, default=0)
    potato_exp = models.PositiveIntegerField(null=False, default=0)

    # Permissions Mixin : 유저의 권한 관리
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "password"]
    objects = (
        UserManager()
    )  # 유저를 생성 및 관리 (유저를 구분해서 관리하기 위해 - 관리자계정, 일반계정)

    def __str__(self):
        """
        오브젝트의 이름을 email로 지정
        """
        return self.email
