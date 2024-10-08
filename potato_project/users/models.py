from common.models import TimeStampedModel
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from potato_types.models import PotatoType
from potatoes.models import Potato


class UserManager(BaseUserManager):
    # 일반 유저 생성 함수
    def create_user(self, username, **extra_fields):
        if not username:
            raise ValueError("The username must be provided")

        user = self.model(username=username, **extra_fields)
        user.set_unusable_password()
        user.save()

        # 감자 생성 로직 추가
        potato_types = PotatoType.objects.all()
        for potato_type in potato_types:
            is_acquired = potato_type.id == 1  # potato_type_id가 1이면 True
            is_selected = potato_type.id == 1  # potato_type_id가 1이면 True
            Potato.objects.create(
                user=user,
                potato_type_id=potato_type.id,
                is_acquired=is_acquired,
                is_selected=is_selected,
            )

        return user

    # 슈퍼 유저 생성 함수
    def create_superuser(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)

        user.is_superuser = True
        user.is_staff = True

        user.set_password(password)  # 비밀번호 해싱
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    # 로그인 관련 필드
    username = models.CharField(max_length=255, null=False, unique=True)
    github_access_token = models.CharField(max_length=255, null=True, blank=True)

    # 프로필 관련 필드
    email = models.CharField(max_length=255, null=True, default="")
    profile_url = models.CharField(max_length=255, null=True)
    github_id = models.CharField(max_length=255, null=True)
    baekjoon_id = models.CharField(max_length=255, null=True, default="")
    nickname = models.CharField(max_length=255, null=False)

    # 감자 관련 필드
    potato_level = models.PositiveIntegerField(null=False, default=1)
    potato_exp = models.PositiveIntegerField(null=False, default=0)
    total_coins = models.PositiveIntegerField(default=0)

    # Permissions Mixin : 유저의 권한 관리
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    # 유저를 생성 및 관리 (유저를 구분해서 관리하기 위해 - 관리자계정, 일반계정)
    objects = UserManager()

    def __str__(self):
        return self.username
