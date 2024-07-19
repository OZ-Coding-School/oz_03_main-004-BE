# github/urls.py
from django.urls import path
from .views import GetCommitDataView

urlpatterns = [
    path('githubs/<int:userid>/commits/', GetCommitDataView.as_view(), name='get_commit_data'),
]
