from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.PotatoesList.as_view(), name="potatoes_list"),
    path("<int:user_id>/", views.PotatoDetail.as_view(), name="potato_detail"),
]
