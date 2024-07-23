from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stack
from .serializers import StackSerializer


# 유저 스택 리스트 조회
class UserStackList(APIView):
    def get(self, request, user_id):
        stacks = Stack.objects.filter(user_id=user_id)
        serializer = StackSerializer(stacks, many=True)
        return Response(serializer.data)
<<<<<<< HEAD


# 유저 스택 리스트 저장
class UserStackCreate(APIView):
    def post(self, request, user_id):
        stacks = Stack.objects.filter(user_id=user_id, data=request.data)
        serializer = StackSerializer(stacks)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
=======
>>>>>>> develop
