from datetime import date, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from githubs.models import Github
from potatoes.models import Potato


@receiver(post_save, sender=Github)
def get_winter_potato(sender, instance, **kwargs):
    # 새 Github 데이터가 생성 or 업데이트, 날짜가 크리스마스이며, commit_num이 >
    if (
        instance.commit_num >= 1
        and instance.date.month == 12
        and instance.date.day == 25
    ):  # 월과 일만 비교
        try:
            # potato_type_id=6인 감자 조회
            potato = Potato.objects.get(user=instance.user, potato_type_id=6)
            if not potato.is_acquired:  # 이미 획득한 경우에는 변경하지 않음
                potato.is_acquired = True
                potato.save()
        except Potato.DoesNotExist:
            # 해당 감자가 없는 경우 에러 처리 (필요에 따라 추가)
            pass


@receiver(post_save, sender=Github)
def get_ghost_potato(sender, instance, **kwargs):
    if (
        instance.commit_num >= 1
        and instance.date.month == 10
        and instance.date.day == 31
    ):
        try:
            potato = Potato.objects.get(user=instance.user, potato_type_id=7)
            if not potato.is_acquired:
                potato.is_acquired = True
                potato.save()
        except Potato.DoesNotExist:
            pass


@receiver(post_save, sender=Github)
def get_crystal_potato(sender, instance, **kwargs):
    if instance.commit_num >= 1:
        # 30일 전 날짜 계산
        thirty_days_ago = instance.date - timedelta(days=30)

        # 30일치 데이터가 있는지 확인
        oldest_record = (
            Github.objects.filter(user=instance.user).order_by("date").first()
        )
        if oldest_record and (instance.date - oldest_record.date).days >= 30:
            # 30일 연속 커밋 여부 확인
            commits_in_30_days = (
                Github.objects.filter(
                    user=instance.user,
                    date__gte=thirty_days_ago,
                    date__lte=instance.date,
                    commit_num__gte=1,
                )
                .values("date")
                .distinct()
                .count()
            )

            if commits_in_30_days == 30:
                try:
                    potato = Potato.objects.get(user=instance.user, potato_type_id=8)
                    if not potato.is_acquired:
                        potato.is_acquired = True
                        potato.save()
                except Potato.DoesNotExist:
                    pass
        else:
            # 30일치 데이터가 없는 경우 로그 남기기 또는 다른 처리
            print(
                f"Not enough data for user {instance.user.id}. Oldest record date: {oldest_record.date if oldest_record else 'No records'}"
            )


@receiver(post_save, sender=Github)
def get_dirty_potato(sender, instance, **kwargs):
    if instance.commit_num == 0:
        # 30일 전 날짜 계산
        thirty_days_ago = instance.date - timedelta(days=30)

        # 30일치 데이터가 있는지 확인
        oldest_record = (
            Github.objects.filter(user=instance.user).order_by("date").first()
        )
        if oldest_record and (instance.date - oldest_record.date).days >= 30:
            # 30일 동안 커밋이 있었는지 확인
            any_commits_in_30_days = Github.objects.filter(
                user=instance.user,
                date__gte=thirty_days_ago,
                date__lte=instance.date,
                commit_num__gte=1,
            ).exists()

            if not any_commits_in_30_days:
                # 30일 연속 커밋이 없는 경우 감자 아이디 9 획득 로직 실행
                try:
                    potato = Potato.objects.get(user=instance.user, potato_type_id=9)
                    if not potato.is_acquired:
                        potato.is_acquired = True
                        potato.save()
                except Potato.DoesNotExist:
                    pass  # 필요에 따라 에러 처리 추가
        else:
            # 30일치 데이터가 없는 경우 로그 남기기 또는 다른 처리
            print(
                f"Not enough data for user {instance.user.id}. Oldest record date: {oldest_record.date if oldest_record else 'No records'}"
            )


@receiver(post_save, sender=Github)
def get_green_potato(sender, instance, **kwargs):
    if instance.commit_num == 0:
        # 90일 전 날짜 계산
        ninety_days_ago = instance.date - timedelta(days=90)

        # 90일치 데이터가 있는지 확인
        oldest_record = (
            Github.objects.filter(user=instance.user).order_by("date").first()
        )
        if oldest_record and (instance.date - oldest_record.date).days >= 90:
            # 90일 동안 커밋이 있었는지 확인
            any_commits_in_90_days = Github.objects.filter(
                user=instance.user,
                date__gte=ninety_days_ago,
                date__lte=instance.date,
                commit_num__gte=1,
            ).exists()

            if not any_commits_in_90_days:
                # 90일 연속 커밋이 없는 경우 감자 아이디 10 획득 로직 실행
                try:
                    potato = Potato.objects.get(user=instance.user, potato_type_id=10)
                    if not potato.is_acquired:
                        potato.is_acquired = True
                        potato.save()
                except Potato.DoesNotExist:
                    pass  # 필요에 따라 에러 처리 추가
        else:
            # 90일치 데이터가 없는 경우 로그 남기기 또는 다른 처리
            print(
                f"Not enough data for user {instance.user.id}. Oldest record date: {oldest_record.date if oldest_record else 'No records'}"
            )
