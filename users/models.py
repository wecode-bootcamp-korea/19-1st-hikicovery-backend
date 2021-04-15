from django.db import models

class User(models.Model):
    account      = models.CharField(max_length=45)
    password     = models.CharField(max_length=300)
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=45)
    phone_number = models.CharField(max_length=45)
    birthday     = models.DateField()
    address      = models.CharField(max_length=100)
    mileage      = models.IntegerField()
    product      = models.ManyToManyField('products.Product',through='reviews.Wishlist')

    class Meta:
        db_table = 'users'





