from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls")),
    path("baekjoons/", include("baekjoons.urls")),
    path("attendances/", include("attendances.urls")),
    path("potatoes/", include("potatoes.urls")),
    path("stacks/", include("stacks.urls")),
    path("stacks/", include("user_stacks.urls")),
]
