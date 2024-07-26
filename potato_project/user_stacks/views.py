from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserStack
from .serializers import UserStackSerializer


# 유저 스택 리스트 조회
class UserStackList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):  # user_id 매개변수 제거
        stacks = UserStack.objects.filter(user=request.user)  # request.user 사용
        serializer = UserStackSerializer(stacks, many=True)
        return Response(serializer.data)


# 유저 스택 리스트 저장
class UserStackCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):  # user_id 매개변수 제거
        serializer = UserStackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # request.user 사용
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 유저 스택 리스트 업데이트
class UserStackPatch(APIView):  # Patch 로 수정
    permission_classes = [IsAuthenticated]

    def patch(self, request):  # user_id 매개변수 제거
        stacks = UserStack.objects.filter(user=request.user)  # request.user 사용

        if not stacks.exists():
            return Response(
                {"error": "No stacks found for this user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        for stack in stacks:
            serializer = UserStackSerializer(stack, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Stacks updated successfully."}, status=status.HTTP_200_OK
        )


# 전체 스택 삭제? -> 하나씩으로 수정 필요
class UserStackDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, stack_id):
        try:
            stack = UserStack.objects.get(user=request.user, id=stack_id)
        except UserStack.DoesNotExist:
            return Response(
                {"error": "Stack not found for this user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        stack.delete()
        return Response(
            {"message": "Stack deleted successfully"}, status=status.HTTP_200_OK
        )