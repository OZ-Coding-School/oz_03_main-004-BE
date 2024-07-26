from django.urls import path

from . import views

urlpatterns = [
    path("", views.MyPotatoDetail.as_view(), name="potato_detail"),
    path(
        "patch/",
        views.PotatoSelectPatch.as_view(),
        name="potato_select_patch",
    ),
]
