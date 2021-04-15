from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    name        = models.CharField(max_length=45)
    price       = models.IntegerField()
    release_at  = models.DateField()
    description = models.TextField()
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    color       = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    season      = models.ManyToManyField('Season', through='ProductSeason')
    size        = models.ManyToManyField('Size', through='ProductDetail')

    class Meta:
        db_table = 'products'

class ProductSale(models.Model):
    product_sales = models.IntegerField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_sales'

class Size(models.Model):
    name = models.IntegerField()

    class Meta:
        db_table = 'sizes'

class Image(models.Model):
    image_url = models.URLField(max_length=500)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_classification = models.ForeignKey('ImageClassification', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'images'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class ProductDetail(models.Model):
    stock   = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_details'
    
class ProductSeason(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    season  = models.ForeignKey('Season', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_seasons'

class Season(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'seasons'

class ImageClassification(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'image_classifications'



