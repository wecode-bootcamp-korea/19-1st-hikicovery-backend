from django.db import models


class Product_Detail_Cart(models.Model):
    quantity       = models.IntegerField()
    product_detail = models.ForeignKey("products.Product_Detail", on_delete=models.CASCADE)
    cart           = models.ForeignKey("Cart", on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_detail_carts'

class Cart(models.Model):
    create_at      = models.DateField(auto_now_add=True)
    updated_at     = models.DateField(auto_now=True)
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product_detail = models.ManyToManyField("products.Product_Detail", through="Product_Detail_Cart")

    class Meta:
        db_table = 'carts'

class Order(models.Model):
    status       = models.CharField(max_length=45)
    pickup       = models.SmallIntegerField()
    create_at    = models.DateField(auto_now_add=True)
    updated_at   = models.DateField(auto_now=True)
    cart         = models.ForeignKey("Cart", on_delete=models.CASCADE)
    user_coupon  = models.ForeignKey("User_Coupon", null=True, on_delete=models.SET_NULL)
    used_mileage = models.IntegerField(null=True)

    class Meta:
        db_table = 'orders'

class User_Coupon(models.Model):
    create_at = models.DateField(auto_now_add=True)
    used_at   = models.DateField(null=True)
    user      = models.ForeignKey("users.User", on_delete=models.CASCADE)
    coupon    = models.ForeignKey("Coupon", on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_coupons'

class Coupon(models.Model):
    name          = models.CharField(max_length=45)
    is_online     = models.SmallIntegerField()
    discount_rate = models.IntegerField()
    duration      = models.IntegerField()
    user          = models.ManyToManyField("users.User", through="User_Coupon")

    class Meta:
        db_table = 'coupons'
