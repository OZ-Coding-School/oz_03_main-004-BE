import requests
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Baekjoon

# 백준 API 불러오는 함수
def get_boj_profile(bj_id):
    url = f"https://solved.ac/api/v3/user/show?handle={bj_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "username": data["handle"],
            "tier": data["tier"],
            "solved_count": data["solvedCount"],
            "rating": data["rating"],
        }
    else:
        return None

# 백준 사용자 이름과 점수를 DB에 저장하는 클래스 기반 뷰
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 인증된 사용자의 백준 아이디를 가져옴
        bj_id = request.user.baekjoon_id
        if not bj_id:
            return JsonResponse({"error": "User does not have a Baekjoon ID."}, status=400)

        profile = get_boj_profile(bj_id)
        if profile:
            # 백준 점수를 데이터베이스에 저장
            Baekjoon.objects.update_or_create(
                user=request.user,
                defaults={
                    "score": profile["solved_count"],
                }
            )
            return JsonResponse(profile)
        else:
            return JsonResponse({"error": "User not found or API error."}, status=404)
