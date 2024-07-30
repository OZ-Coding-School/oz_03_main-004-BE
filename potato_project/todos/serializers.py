from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "task", "is_done", "date"]


class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
          # 생성 시에는 'is_done', 'date'는 자동으로 처리되므로 제외
