from django.urls import path
from carts.views import CartView, OrderView, CouponView

urlpatterns = [
        path('/incart', CartView.as_view()),
        path('/inorder', OrderView.as_view()),
        path('/mycoupon', CouponView.as_view())
        ]
