from django.contrib import admin

from .actions import add_new_potato
from .models import PotatoType


class PotatoTypeAdmin(admin.ModelAdmin):
    actions = [add_new_potato]


admin.site.register(PotatoType, PotatoTypeAdmin)
