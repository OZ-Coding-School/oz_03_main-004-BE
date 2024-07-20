from django.urls import path

from . import views

urlpatterns = [
    path("", views.PotatoesList.as_view(), name="potatoes_list"),
    path("<int:user_id>/", views.MyPotatoDetail.as_view(), name="potato_detail"),
    path(
        "<int:user_id>/patch/",
        views.PotatoSelectPatch.as_view(),
        name="potato_select_patch",
    ),
]
