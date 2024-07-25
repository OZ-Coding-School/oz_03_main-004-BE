from rest_framework.serializers import ModelSerializer

from .models import PotatoType


class PotatoTypeSerializer(ModelSerializer):
    class Meta:
        model = PotatoType
        fields = "__all__"
