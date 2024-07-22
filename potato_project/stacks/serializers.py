from rest_framework.serializers import ModelSerializer

from .models import Stack


class StackSerializer(ModelSerializer):
    class Meta:
        model = Stack
        fields = "__all__"
