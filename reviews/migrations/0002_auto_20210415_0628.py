# Generated by Django 3.1.7 on 2021-04-15 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        ('products', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.AddField(
            model_name='reviewphoto',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review'),
        ),
        migrations.AddField(
            model_name='review',
            name='product_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productdetail'),
        ),
    ]
