import json
from datetime import datetime

from django.http  import JsonResponse
from django.views import View

from carts.models    import ProductDetailOrder, Order, UserCoupon, Coupon
from products.models import ProductDetail, Product, Size, Color
from users.models    import User
from carts.utils     import GetProductDetail
from utils           import login_required


class CartView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        try:
            user     = request.user
            product  = data['product']
            size     = data['size']
            quantity = data['quantity']

            if not Order.objects.filter(status=1, user_id=user.id).exists():
                Order.objects.create(
                        status      = 1,
                        is_delivery = 1,
                        user        = user
                        )

            product_detail = ProductDetail.objects.get(product_id=product, size_id=size)

            if ProductDetailOrder.objects.filter(product_detail_id=product_detail.id, order__user_id=user.id, order__status=1).exists():
                product_detail_order           = ProductDetailOrder.objects.get(product_detail_id=product_detail.id, order__user_id=user.id, order__status=1)    
                product_detail_order.quantity += quantity
                product_detail_order.save()

            else:
                ProductDetailOrder.objects.create(
                    quantity          = quantity,
                    product_detail_id = product_detail.id,
                    order_id          = Order.objects.get(user_id=1, status=1).id
                    )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

    @login_required
    def get(self, request):
        try:
            user = request.user
            show_cart_list = GetProductDetail(user.id)

            return JsonResponse({"MESSAGE" : show_cart_list}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

class OrderView(View):
    @login_required
    def post(self, request):
        datas = json.loads(request.body)
        try:
            user = request.user

            for data in datas:
                product  = data['product']
                size     = data['size']
                quantity = data['quantity']

                product_detail                = ProductDetail.objects.get(product_id=product, size_id=size)
                product_detail_order          = ProductDetailOrder.objects.get(product_detail_id=product_detail.id, order__user_id=user.id, order__status=1)
                product_detail_order.quantity = quantity
                product_detail_order.save()

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

    @login_required
    def get(self, request):
        try:
            user =  request.user
            show_order_list = [{
                    "name"    : user.name,
                    "phone"   : user.phone_number,
                    "email"   : user.email,
                    "address" : user.address,
                    "mileage" : user.mileage,
                    }, GetProductDetail(user.id)]

            return JsonResponse({"MESSAGE" : show_order_list}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)

class Ordered(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = request.user
            now  = datetime.now().strftime('%Y-%m-%d')

            using_mileage = data['using_mileage']
            using_coupon  = data['using_coupon']

            ordered  = Order.objects.get(user=user, status=1)

            if using_mileage != 0:
                ordered.using_mileage = using_mileage
                user.mileage         -= using_mileage
                user.save()

            if using_coupon != 0:
                ordered.user_coupon_id   = now_using_coupon.id
                now_using_coupon         = UserCoupon.objects.get(coupon_id=using_coupon, user_id=user.id)
                now_using_coupon.used_at = now
                now_using_coupon.save()

            ordered.status = 2

            ordered.save()

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)


class CouponView(View):
    @login_required
    def get(self, request):
        try:
            user = request.user
            coupon_list = UserCoupon.objects.filter(user_id=user.id)

            if coupon_list.exists():
                show_coupon_list = [{
                    "name"         : coupons.coupon.name,
                    "is_online"    : coupons.coupon.is_online,
                    "discountrate" : coupons.coupon.discount_rate,
                    "duration"     : coupons.coupon.duration_days
                            } for coupons in coupon_list if not coupons.used_at]
                
                return JsonResponse({"MESSAGE" : show_coupon_list}, status=200)

            return JsonResponse({"MESSAGE" : "No_COUPONS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_EXIST_USER"}, status=400)
