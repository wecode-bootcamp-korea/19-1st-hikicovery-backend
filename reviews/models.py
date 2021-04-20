from django.db import models

class Review(models.Model):
    rating         = models.IntegerField()
    comment        = models.TextField()
    create_at      = models.DateTimeField(auto_now_add=True)
    update_at      = models.DateTimeField(auto_now=True)
    color_review   = models.SmallIntegerField(null=True)
    size_review    = models.SmallIntegerField(null=True)
    product_detail = models.ForeignKey('products.ProductDetail', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class ReviewPhoto(models.Model):
    image_url = models.URLField(max_length=500)
    review    = models.ForeignKey('Review', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review_photos'

class Wishlist(models.Model):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlists'



