from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("dj_rest_auth.urls")),
    path("users/", include("dj_rest_auth.registration.urls")),
    path("users/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("baekjoons/", include("baekjoons.urls")),
    path('attendances/', include('attendances.urls')), 
    path('githubs/', include('githubs.urls')),
    
]
