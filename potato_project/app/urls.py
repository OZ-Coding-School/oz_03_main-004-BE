from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("accounts/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("api/baekjoons/", include("baekjoons.urls")),
    path("api/attendances/", include("attendances.urls")),
    path("api/potatoes/", include("potatoes.urls")),
    path("api/potatoes/", include("potato_types.urls")),
    path("api/stacks/", include("stacks.urls")),
    path("api/stacks/", include("user_stacks.urls")),
    path("api/todos/", include("todos.urls")),
    path("api/githubs/", include("githubs.urls")),
]
