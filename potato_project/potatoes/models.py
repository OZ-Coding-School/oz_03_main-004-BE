from common.models import TimeStampedModel
from django.db import models


class Potato(TimeStampedModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    potato_type_id = models.ForeignKey(
        "potato_type.PotatoType", on_delete=models.CASCADE
    )
    is_acquired = models.BooleanField(blank=True, null=True)
    is_selected = models.BooleanField(blank=True, null=True)
