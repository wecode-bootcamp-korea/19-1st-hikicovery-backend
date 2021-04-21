from django.urls import path
from products.views import ProductDetailView, BestItemView, ProductView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/best-items', BestItemView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]