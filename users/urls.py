from django.urls import (path)
from users.views import SignUpView,LogInView
from carts.views import CouponView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LogInView.as_view()),
    path('/mycoupon', CouponView.as_view())
    ]
