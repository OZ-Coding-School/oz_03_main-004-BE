from django.contrib import messages
from potatoes.models import Potato
from users.models import User

from .models import PotatoType


def add_new_potato(modeladmin, request, queryset):
    new_potato_type = queryset.first()  # Admin에서 선택한 PotatoType 객체 가져오기
    if not new_potato_type:
        messages.error(request, "새로운 감자 종류를 선택해주세요.")
        return

    for user in User.objects.filter(is_superuser=False):
        Potato.objects.create(
            user=user,
            potato_type_id=new_potato_type.id,
            is_acquired=False,
            is_selected=False,
        )

    messages.success(request, f"모든 유저에게 '{new_potato_type.potato_name}' 감자가 추가되었습니다.")
