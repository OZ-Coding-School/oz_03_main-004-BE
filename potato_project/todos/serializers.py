# serializers.py
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "task", "is_done", "date"]
        read_only_fields = ["user"]
