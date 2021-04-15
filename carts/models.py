from django.db import models


class ProductDetailCart(models.Model):
    quantity       = models.IntegerField()
    product_detail = models.ForeignKey("products.ProductDetail", on_delete=models.CASCADE)
    cart           = models.ForeignKey("Cart", on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_detail_carts'

class Cart(models.Model):
    create_at      = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product_detail = models.ManyToManyField("products.ProductDetail", through="ProductDetailCart")

    class Meta:
        db_table = 'carts'

class Order(models.Model):
    status       = models.CharField(max_length=45)
    is_delivery  = models.SmallIntegerField()
    create_at    = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    cart         = models.ForeignKey("Cart", on_delete=models.CASCADE)
    user_coupon  = models.ForeignKey("UserCoupon", null=True, on_delete=models.SET_NULL)
    using_mileage = models.IntegerField(default=0)

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
