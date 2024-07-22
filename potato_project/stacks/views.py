from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stack
from .serializers import StackSerializer


# 전체 스택 리스트 조회
class StackList(APIView):
    def get(self, request):
        stacks = Stack.objects.all()
        serializer = StackSerializer(stacks, many=True)
        return Response(serializer.data)
    