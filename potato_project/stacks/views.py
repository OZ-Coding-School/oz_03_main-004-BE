from rest_framework.views import APIView
from rest_framwork.response import Response

from .models import Stack
from .serializers import StackSerializer


# 전체 스택 조회
class StackList(APIView):
    def get(self, request):
        stacks = Stack.objects.all()
        serializer = StackSerializer(stacks, many=True)
        return Response(serializer.data)
