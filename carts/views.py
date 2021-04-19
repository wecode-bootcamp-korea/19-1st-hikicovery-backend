import json

from django.http import JsonResponse
from django.views import View

from carts.models import ProductDetailOrder, Order, UserCoupon, Coupon

from products.models import ProductDetail, Product, Size, Color

from users.models import User

from carts.utils import GetProductDetail


class CartView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
#            user_id = request.user
            user = User.objects.get(id=1)   # 데코레이터에서 id=1인 유저를 받아온다 가정

            if not Order.objects.filter(status=1, user_id=user):
                Order.objects.create(
                        status      = 1,
                        is_delivery = 1,
                        user        = user
                        )
            this_product         = Product.objects.get(name=data['product'], color=Color.objects.get(name=data['color']))
            this_size            = Size.objects.get(name=data['size'])
            product_detail       = ProductDetail.objects.get(product_id=this_product.id, size_id=this_size.id)
            try:
                if product_detail_order := ProductDetailOrder.objects.get(product_detail_id=product_detail.id, order_id=Order.objects.get(user_id=user.id, status=1).id):
                    product_detail_order.quantity = int(product_detail_order.quantity) + int(data['quantity'])
                    product_detail_order.save()
            except:
                ProductDetailOrder.objects.create(
                    quantity          = data['quantity'],
                    product_detail_id = product_detail.id,
                    order_id          = Order.objects.get(user_id=1, status=1).id
                    )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

    def get(self, request):
        try:
#            user_id = request.user
            user = User.objects.get(id=1)   # 데코레이터에서 id=1인 유저를 받아온다 가정

            show_cart_list = GetProductDetail(user.id)

            return JsonResponse({"MESSAGE" : show_cart_list}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

class OrderView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=1)

            for this_data in data:
                order_product        = Product.objects.get(name=this_data['product'], color=Color.objects.get(name=this_data['color']))
                order_size           = Size.objects.get(name=this_data['size'])
                product_detail       = ProductDetail.objects.get(product_id=order_product.id, size_id=order_size.id)
                product_detail_order = ProductDetailOrder.objects.get(product_detail_id=product_detail.id, order_id=Order.objects.get(user_id=user.id, status=1).id)
                product_detail_order.quantity = this_data['quantity']
                product_detail_order.save()

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)


    def get(self, request):
        try:
            user = User.objects.get(id=1)

            show_order_list = []

            show_cart_list = GetProductDetail(user.id)

            order_user_info = {
                    "name"    : user.name,
                    "phone"   : user.phone_number,
                    "email"   : user.email,
                    "address" : user.address,
                    "mileage" : user.mileage,
                    }

            show_order_list.append(order_user_info)
            show_order_list.append(show_cart_list)

            return JsonResponse({"MESSAGE" : show_order_list}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

class CouponView(View):
    def get(self, request):
        try:
            user = 1
            show_coupon_list = []

            coupon_list=UserCoupon.objects.filter(user_id=user)

            if counpon_list:
                for coupons in coupon_list:
                    if not coupons.used_at:
                        show_coupon_list.append({
                            "name"        : coupons.coupon.name,
                            "is_online"   : coupons.coupon.is_online,
                            "discountrate": coupons.coupon.discount_rate,
                            "duration"    : coupons.coupon.duration
                            })

            return JsonResponse({"MESSAGE" : show_coupon_list}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)


