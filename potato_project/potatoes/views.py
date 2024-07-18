from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Potato
from .serializers import PotatoSerializer


# 전체 감자 목록 조회
class PotatoesList(APIView):
    def get(self, request):
        potatoes = Potato.objects.all()
        serializer = PotatoSerializer(potatoes, many=True)
        return Response(serializer.data)
    
class PotatoDetail(APIView):
    def get(self, request):
        potato = Potato.objects.filter(user=request.user)
        serializer = PotatoSerializer(potato)
        return Response(serializer.data)
