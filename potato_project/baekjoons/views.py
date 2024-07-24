import requests
from django.http import JsonResponse
from django.shortcuts import render
from .models import Baekjoon  # Baekjoon 모델 임포트

#백준 api 불러오는 내용 수정하는 함수
def get_boj_profile(userid):
    url = f"https://solved.ac/api/v3/user/show?handle={userid}"  
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

#백준 사용자 이름과 점수를 db에 저장하는 함수
def profile_view(request, userid):
    profile = get_boj_profile(userid)
    if profile:
        # 데이터베이스에 저장
        Baekjoon.objects.update_or_create(
            user=request.user,  # baekjoons/models.py에 user을 참조함
            defaults={
                "bj_name": profile["username"],
                "score": profile["solved_count"],  # solved_count를 score 필드에 저장
            }
        )
        return JsonResponse(profile)
    else:
        return JsonResponse({"error": "User not found or API error."}, status=404)
