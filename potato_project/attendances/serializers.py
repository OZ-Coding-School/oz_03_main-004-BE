# attendances/serializers.py
from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["user_id", "date", "coin_awarded"]
