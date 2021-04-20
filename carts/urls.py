from django.urls import path
from carts.views import OrderView, CouponView

urlpatterns = [
        path('', OrderView.as_view()),
        path('/mycoupon', CouponView.as_view())
        ]
