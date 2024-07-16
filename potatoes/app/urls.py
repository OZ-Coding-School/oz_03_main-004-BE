from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('dj_rest_auth.urls')),
    path('users/', include('dj_rest_auth.registration.urls')),
    path('users/', include('allauth.urls')),
    # path('users/', include('users.urls')),
]
