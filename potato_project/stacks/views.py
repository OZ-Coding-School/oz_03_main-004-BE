<<<<<<< HEAD
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
=======
from rest_framework.views import APIView
from rest_framwork.response import Response
>>>>>>> 7958cf4 (<FEAT>: UserStackList 생성)

from .models import Stack
from .serializers import StackSerializer


<<<<<<< HEAD
# 유저 스택 리스트 조회
class UserStackList(APIView):
    def get(self, request, user_id):
        stacks = Stack.objects.filter(user_id=user_id)
        serializer = StackSerializer(stacks, many=True)
        return Response(serializer.data)


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
# 전체 스택 조회
class StackList(APIView):
    def get(self, request):
        stacks = Stack.objects.all()
        serializer = StackSerializer(stacks, many=True)
        return Response(serializer.data)
>>>>>>> 7958cf4 (<FEAT>: UserStackList 생성)
