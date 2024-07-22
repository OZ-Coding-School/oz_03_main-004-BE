from rest_framework.serializers import ModelSerializer

from ..stacks.models import Stack


class StackSerializer(ModelSerializer):
    class Meta:
        model = Stack
        fields = "__all__"
