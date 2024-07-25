from common.models import TimeStampedModel
from django.db import models
from potato_types.models import PotatoType
from users.models import User


class Potato(TimeStampedModel):
    # id제거
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    potato_type_id = models.ForeignKey(PotatoType, on_delete=models.CASCADE)
    is_acquired = models.BooleanField(blank=True, null=True)
    is_selected = models.BooleanField(blank=True, null=True)
