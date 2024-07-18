from common.models import TimeStampedModel
from django.db import models
from potato_types.models import PotatoType
from users.models import User


class Potato(TimeStampedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    potato_type_id = models.ForeignKey(PotatoType, on_delete=models.CASCADE)
    is_selected = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.potato_nickname or "Unnamed Potato"
