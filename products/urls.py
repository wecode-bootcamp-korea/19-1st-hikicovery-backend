from django.urls import path
from products.views import ProductView, MajorView, ProductCategoryView

urlpatterns = [
    path('/display/categoryview', ProductCategoryView.as_view()),
    path('/goods/<int:product_id>', ProductView.as_view())
]