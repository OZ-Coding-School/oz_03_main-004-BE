from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserStack
from .serializers import UserStackSerializer


# 유저 스택 리스트 조회
class UserStackList(APIView):
    def get(self, request, user_id):
        stacks = UserStack.objects.filter(user_id=user_id)
        serializer = UserStackSerializer(stacks, many=True)
        return Response(serializer.data)


# 유저 스택 리스트 저장
class UserStackCreate(APIView):
    def post(self, request, user_id):
        stacks = UserStack.objects.filter(user_id=user_id, data=request.data)
        serializer = UserStackSerializer(stacks)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 유저 스택 리스트 업데이트
class UserStackPacth(APIView):
    def patch(self, request, user_id):
        stacks = UserStack.objects.filter(user_id=user_id, data=request.data)
        
        if not stacks.exists():
            return Response({"error": "No stacks found for this user"}, status=status.HTTP_404_NOT_FOUND)
    
        for stack in stacks:
            serializer = UserStackSerializer(stack, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": "Stacks updated successfully."}, status=status.HTTP_200_OK)
    

# class UserStackDelete(APIView):
#     def delete(self, request, user_id):
#         stacks = UserStack.objects.filter(user_id=user_id)

#         if not stacks.exists():
#             return Response({"error": "No stacks found for this user"}, status=status.HTTP_404_NOT_FOUND)
        
#         stacks.delete()
#         return Response({"message": "Stacks deleted successflully"}, status=status.HTTP_200_OK)