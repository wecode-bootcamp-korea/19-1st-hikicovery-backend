import json

from django.http            import JsonResponse
from django.views           import View
from products.models        import Product,ProductDetail
from carts.models           import ProductDetailOrder,Order
from users.models           import User
from models                 import Review,ReviewPhoto,Wishlist
from utils                  import login_required

@login_required
class ReviewCreateView(View):
    def post(self,request):
        data=json.loads(request.body)

        rating         = data['rating']
        comment        = data['comment']
        color_review   = data['color_review']
        size_review    = data['size_review']
        product_detail = ProductDetail.objects.get(product_id=data['product_id'], size_id=data['size_id']).id
        image_url      = data.get('image_url', None)
        review_id      =

        review = Review.objects.create(
                 rating         = rating,
                 comment        = comment,
                 color_review   = color_review,
                 size_review    = size_review,
                 product_detail = product_detail
                 )

        ReviewPhoto.objects.create(
                 image_url=image_url,
                 review_id=review.id
                 )

class ReviewShowView(View):
    def get(self,request):
        data=json.loads(request.body)

        if ProductDetail.objects.get(product__name=data['product']).exists():
            review_photo=[photo for photo in ReviewPhoto.objects.filter(review_id=data['review_id'])]

            data = {
                'rating'        : Review.rating,
                'comment'       : Review.comment,
                'color_review'  : Review.color_review,
                'size_review'   : Review.size_review,
                'create_at'     : Review.create_at,
                'update_at'     : Review.update_at,
                'product_detail': Review.product_detail,
                'review_photo'  : review_photo.image_url,
                'size'          : ProductDetail.size_id,
                'color'         : Product.color_id

            }
        return JsonResponse({'data': json.dumps(data)}, status=200)

class WishListCreateView(View):
    def post(self,request):
        data = json.loads(request.body)

        Wishlist.objects.create(
            user_id    = User.objects.get(user_id = User.id),
            product_id = Product.objects.get(product_id = Product.id)
        )

class WishListShowView(View):
    def get(self,request):
        data = json.loads(request.body)

        return JsonResponse({'data': json.dumps(data)}, status=200)


