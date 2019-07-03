from django.urls import path

from . import sudokuViews

urlpatterns = [
    path("", sudokuViews.index, name="index"),
    path("history", sudokuViews.index, name="index"),
    path("api/analyze", sudokuViews.analyze, name="analyze"),
]
