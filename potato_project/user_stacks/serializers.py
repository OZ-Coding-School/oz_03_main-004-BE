from rest_framework.serializers import ModelSerializer

from user_stacks.models import UserStack


class UserStackSerializer(ModelSerializer):
    class Meta:
        model = UserStack
        fields = "__all__"
