from django.urls import path, include
from reviews.views import ReviewView
from utils      import login_required

urlpatterns = [
    path('/<int:product_id>', ReviewView.as_view()),
    path('/review',ReviewView.as_view()),
    ]