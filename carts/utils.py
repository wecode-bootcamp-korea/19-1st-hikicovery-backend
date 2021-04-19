from django.db import models

from carts.models import ProductDetailOrder, Order

from products.models import Product, ProductDetail, Image

def GetProductDetail(this_id):
    this_order_product = ProductDetailOrder.objects.filter(order__status=1, order__user_id=this_id)
    '''
    Order 내 status 
    1: 장바구니
    2: 결제대기
    3: 결제완료
    4: 상품준비
    5: 배송시작
    6: 배송완료
    '''
    products_list = []

    for products in this_order_product:
        name     = products.product_detail.product.name
        size     = products.product_detail.size.name
        color    = products.product_detail.product.color.name
        price    = products.product_detail.product.price
        quantity = products.quantity
        image    = products.product_detail.product.image_set.get(image_classification_id=1).image_url
        products_list.append({
            "name"     : name,
            "size"     : size,
            "color"    : color,
            "price"    : price,
            "quantity" : quantity,
            "image"    : image
            })
    
    return products_list
