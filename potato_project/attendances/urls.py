from django.urls import include, path
# url을 보는데 아래 토큰을 발급받는과정이 로그인 이후 출석을 하는데 필요한 과정이라고 나오는데
# 잘모르겠어서 이건 다같이 봐주면 좋겟음..이게 로그인할때 받은 코드를 활용하는건지를 잘 모르겟슴
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
