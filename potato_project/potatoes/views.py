from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Potato
from .serializers import PotatoSerializer


# 유저의 감자 조회
class MyPotatoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            potato = Potato.objects.filter(user=request.user)  # request.user 사용
            if not potato.exists():
                raise ObjectDoesNotExist(
                    f"No potatoes found for user {request.user}"
                )  # request.user 사용

            serializer = PotatoSerializer(potato, many=True)
        # 데이터베이스 연결 또는 쿼리 오류 처리
        except DatabaseError as e:
            return Response(
                {"error": "DB 에러 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # 시리얼라이저 오류 처리
        except ValidationError as e:
            return Response(
                {"error": "Serializer 에러 발생", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 객체가 존재하지 않을 때의 오류 처리
        except ObjectDoesNotExist as e:
            return Response(
                {"error": "object가 존재하지 않습니다", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        # 기타 일반 예외 처리
        except Exception as e:
            return Response(
                {"error": "예기치 않은 오류가 발생했습니다", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.data)


# 유저의 감자 선택 상태 변경
class PotatoSelectPatch(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            potato_id = request.data.get("id")
            potato = Potato.objects.get(id=potato_id, user=request.user)

            if not potato:
                return Response(
                    {"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # 기존에 선택된 감자의 is_selected 값을 False로 변경
            Potato.objects.filter(user=request.user).update(is_selected=False)
            # 현재 선택된 감자의 is_selected 값을 True로 변경
            potato.is_selected = True  # 객체 속성 직접 변경
            potato.save()  # 변경 사항 저장

            serializer = PotatoSerializer(potato)  # 업데이트된 객체 다시 가져오기
            return Response(serializer.data)

        except Exception as e:  # Exception handling remains the same
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
