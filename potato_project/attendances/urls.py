from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AttendanceViewSet

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", AttendanceViewSet.as_view({'get': 'list'}), name="attendance-list"),
    path("increment/", AttendanceViewSet.as_view({'post': 'increment'}), name="attendance-increment"),
    path("decrement/", AttendanceViewSet.as_view({'post': 'decrement'}), name="attendance-decrement"),
]
