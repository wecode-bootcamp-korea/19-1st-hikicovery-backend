from django.db import models


class ProductDetailOrder(models.Model):
    quantity       = models.IntegerField()
    product_detail = models.ForeignKey("products.ProductDetail", on_delete=models.CASCADE)
    order          = models.ForeignKey("Order", on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_detail_orders'

class Order(models.Model):
    status          = models.SmallIntegerField()
    is_delivery     = models.SmallIntegerField()
    create_at       = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    cart            = models.ForeignKey("Cart", on_delete=models.CASCADE)
    user_coupon     = models.ForeignKey("UserCoupon", null=True, on_delete=models.SET_NULL)
    using_mileage   = models.IntegerField(default=0)
    product_detail  = models.ManyToManyField("products.ProductDetail", through="ProductDetailOrder")
    user          = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class UserCoupon(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    used_at   = models.DateField(null=True)
    user      = models.ForeignKey("users.User", on_delete=models.CASCADE)
    coupon    = models.ForeignKey("Coupon", on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_coupons'

class Coupon(models.Model):
    name          = models.CharField(max_length=45)
    is_online     = models.SmallIntegerField()
    discount_rate = models.IntegerField()
    duration_days = models.IntegerField()
    user          = models.ManyToManyField("users.User", through="UserCoupon")

    class Meta:
        db_table = 'coupons'
