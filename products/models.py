from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    name        = models.CharField(max_length=45)
    price       = models.IntegerField()
    release_at  = models.DateField()
    sales_rate  = models.IntegerField()
    description = models.TextField()
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    color       = models.ForeignKey('Color', on_delete=models.CASCADE)
    season      = models.ManyToManyField('Season', through='Product_Season')
    size        = models.ManyToManyField('Size', through='Product_Detail')

    class Meta:
        db_table = 'products'

class Size(models.Model):
    size = models.IntegerField()

    class Meta:
        db_table = 'sizes'

class Image(models.Model):
    image_url = models.CharField(max_length=500)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'images'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Product_Detail(models.Model):
    stock   = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_details'
    
class Product_Season(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    season  = models.ForeignKey('Season', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_seasons'

class Season(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'seasons'





