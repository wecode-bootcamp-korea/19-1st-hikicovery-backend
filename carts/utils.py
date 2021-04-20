from django.db import models

from carts.models import ProductDetailOrder, Order

from products.models import Product, ProductDetail, Image

def GetProductDetail(user_id):
    user_order_product = ProductDetailOrder.objects.filter(order__status=1, order__user_id=user_id)
    products_list = [{
            "name"     : products.product_detail.product.name,
            "size"     : products.product_detail.size.name,
            "color"    : products.product_detail.product.color.name,
            "price"    : products.product_detail.product.price,
            "quantity" : products.quantity,
            "image"    : products.product_detail.product.image_set.get(image_classification_id=1).image_url
            } for products in user_order_product]

    return products_list
