from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Potato
from .serializers import PotatoSerializer


# 전체 감자 목록 조회
class PotatoesList(APIView):
    def get(self, request):
        potatoes = Potato.objects.all()
        serializer = PotatoSerializer(potatoes, many=True)
        return Response(serializer.data)


# 유저의 감자 하나 조회
class MyPotatoDetail(APIView):
    def get(self, request, user_id):
        potato = Potato.objects.filter(user_id=user_id)


# 유저의 감자 선택 상태 변경
class PotatoSelectPatch(APIView):
    def patch(self, request, user_id):
        potato = Potato.objects.filter(user_id=user_id, data=request.data, partial=True)

        if not potato:
            return Response({"detail" : "Not found"}, status=status.HTTP_404_NOT_FOUND)

        if "is_selected" in request.data:
            is_selected = request.data["is_selected"]
            if is_selected:
                # 유저가 가지고 있는 모든 감자 is_selected 값을 False로
                Potato.objects.filter(user_id=user_id).update(is_selected=False)
            # 유저가 선택한 감자의 is_selected 값을 True로
            serializer = PotatoSerializer(potato, data={"is_selected": is_selected}, partial=True)
        else:
            return Response({"detail": "is_selected field is required"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)