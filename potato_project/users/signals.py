from django.db.models.signals import post_save
from django.dispatch import receiver
from potatoes.models import Potato
from users.models import User


@receiver(post_save, sender=User)
def get_level_two_potato(sender, instance, **kwargs):
    # 레벨이 2로 변경되었고, 이전 레벨이 2가 아닐 때만 실행
    if (
        instance.potato_level == 2
        and instance.tracker.has_changed('potato_level')
        and instance.tracker.previous("potato_level") != 2
        and not kwargs.get("created", False)
    ):
      	try:
            # potato_type_id=2인 감자 조회
            potato = Potato.objects.get(user=instance.user, potato_type_id=2)
            if not potato.is_acquired:
                potato.is_acquired = True
                potato.save()
        except Potato.DoesNotExist:
            # 해당 감자가 없는 경우 에러 처리 (필요에 따라 추가)
            pass



@receiver(post_save, sender=User)
def get_level_three_potato(sender, instance, **kwargs):
    if (
        instance.potato_level == 3
        and instance.tracker.has_changed('potato_level')
        and instance.tracker.previous("potato_level") != 3
        and not kwargs.get("created", False)
    ):
        try:
            potato = Potato.objects.get(user=instance.user, potato_type_id=3)
            if not potato.is_acquired:
                potato.is_acquired = True
                potato.save()
        except Potato.DoesNotExist:
            pass


@receiver(post_save, sender=User)
def get_level_four_potato(sender, instance, **kwargs):
    if (
        instance.potato_level == 4
        and instance.tracker.previous("potato_level") != 4
        and instance.tracker.has_changed('potato_level')
        and not kwargs.get("created", False)
    ):
      	try:
            potato = Potato.objects.get(user=instance.user, potato_type_id=4)
            if not potato.is_acquired:
                potato.is_acquired = True
                potato.save()
        except Potato.DoesNotExist:
            pass



@receiver(post_save, sender=User)
def get_level_five_potato(sender, instance, **kwargs):
    if (
        instance.potato_level == 5
        and instance.tracker.has_changed('potato_level')
        and instance.tracker.previous("potato_level") != 5
        and not kwargs.get("created", False)
    ):
      	try:
            potato = Potato.objects.get(user=instance.user, potato_type_id=5)
            if not potato.is_acquired:
                potato.is_acquired = True
                potato.save()
        except Potato.DoesNotExist:
            pass

