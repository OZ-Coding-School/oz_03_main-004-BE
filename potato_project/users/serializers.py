from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username", "profile_url", "github_id", "baekjoon_id"]
