# baekjoons/views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests

def get_boj_profile(userid):
    url = f"https://solved.ac/api/v3/user/show?handle={userid}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "username": data["handle"],
            "tier": data["tier"],
            "solved_count": data["solvedCount"],
            "rating": data["rating"]
        }
    else:
        return None

def profile_view(request, userid):
    profile = get_boj_profile(userid)
    if profile:
        return JsonResponse(profile)
    else:
        return JsonResponse({"error": "User not found or API error."}, status=404)
