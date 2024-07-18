from django.shortcuts import render
from django.http import JsonResponse
import requests


# solved.ac에서 api를 받아오는 함수, 더 필요할 시 추가 할 예정
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


# 유저 아이디를 입력해서 solved에 개인 아이디 입력하는 함수
def profile_view(request, userid):
    profile = get_boj_profile(userid)
    if profile:
        return JsonResponse(profile)
    else:
        return JsonResponse({"error": "User not found or API error."}, status=404)
