from django.urls import re_path, path
from . import views

app_name = "shortener"

urlpatterns = [
    re_path(r"^.+", views.index.as_view(), name="index"),
]