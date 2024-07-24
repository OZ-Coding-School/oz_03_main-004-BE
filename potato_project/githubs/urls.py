from django.urls import path
from .views import GetCommitDataView

urlpatterns = [
    path('commits/', GetCommitDataView.as_view(), name='get_commit_data'),
]
