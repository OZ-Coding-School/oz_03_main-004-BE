from django.urls import path

from .views import ProfileView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile_view"),
]
