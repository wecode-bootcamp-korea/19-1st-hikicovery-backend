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
            user = User.objects.get(id=1)

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

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

    def get(self, request):
        try:
            user = User.objects.get(id=1)

            show_cart_list = GetProductDetail(user.id)

            return JsonResponse({"MESSAGE" : show_cart_list}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

class OrderView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=1)

            for this_data in data:
                product  = this_data['product']
                color    = this_data['color']
                size     = this_data['size']
                quantity = this_data['quantity']
                order_product        = Product.objects.get(name=product, color=Color.objects.get(name=color))
                order_size           = Size.objects.get(name=size)
                product_detail       = ProductDetail.objects.get(product_id=order_product.id, size_id=order_size.id)
                product_detail_order = ProductDetailOrder.objects.get(product_detail_id=product_detail.id, order_id=Order.objects.get(user_id=user.id, status=1).id)
                product_detail_order.quantity = quantity
                product_detail_order.save()

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

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

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

class CouponView(View):
    def get(self, request):
        try:
            user = User.objects.get(id=1)
            show_coupon_list = []

            coupon_list=UserCoupon.objects.filter(user_id=user.id)

            if counpon_list.exists():
                show_coupon_list = [{
                    "name"        : coupons.coupon.name,
                    "is_online"   : coupons.coupon.is_online,
                    "discountrate": coupons.coupon.discount_rate,
                    "duration"    : coupons.coupon.duration
                            } for coupons in coupon_list if not coupons.used_at]

            return JsonResponse({"MESSAGE" : show_coupon_list}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)


