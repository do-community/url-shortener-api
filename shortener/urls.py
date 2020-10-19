from django.urls import re_path, path
from . import views

app_name = "shortener"

urlpatterns = [
    path("manage/", views.redir_admin.as_view(), name="manage"),
    path("manage/<str:short_link>/", views.redir_admin.as_view(), name="manage_delete"),
    re_path(r"^.+", views.index.as_view(), name="index"),
]