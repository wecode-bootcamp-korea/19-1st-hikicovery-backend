from django.urls import (path)
from reviews.views import ReviewCreateView, ReviewShowView

urlpatterns = [
    path('/create', ReviewCreateView.as_view()),
    path('/show', ReviewShowView.as_view()),
    ]