from django.urls import path
from users import views

urlpatterns = [
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),  
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    path('github/login/', views.github_login, name='github_login'),
    path('github/callback/', views.github_callback, name='github_callback'),
    path('github/login/finish/', views.GithubLogin.as_view(), name='github_login_todjango'),
]