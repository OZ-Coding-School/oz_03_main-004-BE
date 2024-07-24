from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import DatabaseError
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from .models import Potato
from .serializers import PotatoSerializer


# 전체 감자 목록 조회
class PotatoesList(APIView):
    def get(self, request):
        try:    
            potatoes = Potato.objects.all()
            serializer = PotatoSerializer(potatoes, many=True)
        # DB 연결 또는 쿼리 오류
        except DatabaseError as e:
            return Response({"error": "DB 에러 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 시리얼라이저 오류 처리
        except ValidationError as e:
            return Response({"error": "Serializer 에러 발생", "details": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        # 객체가 존재하지 않을 때의 오류
        except ObjectDoesNotExist as e:
            return Response({"error": "object가 존재하지 않습니다", "details": str(e)}, status=status.HTTP_404_NOT_FOUND)
        # 기타 일반 예외 처리
        except Exception as e:
            return Response({"error": "예기치 않은 오류가 발생했습니다", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        return Response(serializer.data)


# 유저의 감자 하나 조회
class MyPotatoDetail(APIView):
    def get(self, request, user_id):
        try:
            potato = Potato.objects.filter(user_id=user_id)
            if not potato.exists():
                raise ObjectDoesNotExist(f"No potatoes found for user_id {user_id}")

            serializer = PotatoSerializer(potato, many=True)  # 나중에 many=True 옵션 삭제
        # 데이터베이스 연결 또는 쿼리 오류 처리
        except DatabaseError as e:
            return Response({'error': 'DB 에러 발생'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 시리얼라이저 오류 처리
        except ValidationError as e:
            return Response({'error': 'Serializer 에러 발생', 'details': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        # 객체가 존재하지 않을 때의 오류 처리
        except ObjectDoesNotExist as e:
            return Response({'error': 'object가 존재하지 않습니다', 'details': str(e)}, status=status.HTTP_404_NOT_FOUND)
        # 기타 일반 예외 처리
        except Exception as e:
            return Response({'error': '예기치 않은 오류가 발생했습니다', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data)


# 유저의 감자 선택 상태 변경
class PotatoSelectPatch(APIView):
    def patch(self, request, user_id):
        try:
            potato = Potato.objects.filter(user_id=user_id, data=request.data, partial=True)
            
            if not potato.exists():
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

            if "is_selected" not in request.data:
                return Response(
                    {"detail": "is_selected field is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            is_selected = request.data["is_selected"]
            if is_selected:
                # 유저가 가지고 있는 모든 감자의 is_selected 값을 False로
                Potato.objects.filter(user_id=user_id).update(is_selected=False)
            
            # 유저가 선택한 감자의 is_selected 값을 True로
            serializer = PotatoSerializer(
                potato.first(), data={"is_selected": is_selected}, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except DatabaseError as e:
            return Response({'error': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({'error': 'Serialization error occurred', 'details': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({'error': 'Object does not exist', 'details': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
