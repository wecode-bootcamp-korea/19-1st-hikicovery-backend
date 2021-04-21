import json

from django.http            import JsonResponse
from django.views           import View
from products.models        import Product,ProductDetail
from users.models           import User
from carts.models           import Order
from reviews.models         import Review,ReviewPhoto,Wishlist
from utils                  import login_required

@login_required
class ReviewCreateView(View):
    def post(self,request):
        data=json.loads(request.body)

        if not Order.objects.get(id=data['order_id']).exists():
            return JsonResponse({'message': 'INVALID_REQUEST'}, status=400)

        rating         = data['rating']
        comment        = data['comment']
        color_review   = data['color_review']
        size_review    = data['size_review']
        product_detail = data['product_detail_id']
        user_id        = data['user_id']

        Review.objects.create(
            rating         = rating,
            comment        = comment,
            color_review   = color_review,
            size_review    = size_review,
            product_detail = product_detail,
            user_id        = user_id
            )

        image_url = data.get('image_url', None)
        review = Review.objects.get(user_id=user_id, product_detail=product_detail)

        ReviewPhoto.objects.create(
                 image_url = image_url,
                 review    = review,
                 )
        return JsonResponse({'message':'REVIEW_POSTED'},status=200)

class ReviewShowView(View):
    def get(self,request):
        data = json.loads(request.body)

        if not Product.objects.filter(name=data['product_name']).exists():
            return JsonResponse({'message':'ITEM_NOT_EXIST'})

        product_review = Review.objects.get(id = data['review_id'])

        data = {
            'rating'        : product_review.rating,
            'comment'       : product_review.comment,
            'color_review'  : product_review.color_review,
            'size_review'   : product_review.size_review,
            'create_at'     : product_review.create_at,
            'update_at'     : product_review.update_at,
            'product_detail': product_review.product_detail,
            'review_photo'  : [photo for photo in ReviewPhoto.objects.filter(review=data['review_id'])],
            'size'          : product_review.product_detail.product.size,
            'color'         : product_review.product_detail.product.color,
        }

        return JsonResponse({'data': data}, status=200)

#class WishListCreateView(View):
#    def post(self,request):
#        data = json.loads(request.body)
#
#        Wishlist.objects.create(
#            user_id    = User.objects.get(id=data['user_id']).account,
#            product_id = Product.objects.get(id=data['product_id']).name,
#        )
#
#class WishListShowView(View):
#    def get(self,request):
#
#
#
#        return JsonResponse({'data': data}, status=200)


