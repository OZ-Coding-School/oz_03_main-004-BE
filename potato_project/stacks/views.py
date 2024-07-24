from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framwork.exceptions import ValidationError

from .models import Stack
from .serializers import StackSerializer


# 유저 스택 리스트 조회
class UserStackList(APIView):
    def get(self, request, user_id):
        try:
            stacks = Stack.objects.filter(user_id=user_id)
            serializer = StackSerializer(stacks, many=True)
        # DB 연결 또는 쿼리 오류
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
        except ObjectDoesNotExist as e:
            return Response(
                {"error": "object가 존재하지 않습니다", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": "예기치 않은 오류가 발생했습니다", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(serializer.data)


# 유저 스택 리스트 저장
class UserStackCreate(APIView):
    def post(self, request, user_id):
        try:
            stacks = Stack.objects.filter(user_id=user_id, data=request.data)
            serializer = StackSerializer(stacks)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # DB 연결 또는 쿼리 오류
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
        # 객체가 존재하지 않을 때의 오류
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
