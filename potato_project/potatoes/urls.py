from django.urls import path

from . import views

urlpatterns = [
    path("collection/", views.MyPotatoDetail.as_view(), name="potato_detail"),
    path(
        "select/",
        views.PotatoSelectPatch.as_view(),
        name="potato_select_patch",
    ),
]
