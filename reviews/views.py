import json

from django.http            import JsonResponse
from django.views           import View
from products.models        import Product,ProductDetail
from users.models           import User
from carts.models           import Order
from reviews.models         import Review,ReviewPhoto
from utils                  import login_required


class ReviewView(View):
    #@login_required
    def post(self,request):
        data=json.loads(request.body)

        rating         = data['rating']
        comment        = data['comment']
        color_review   = data['color_review']
        size_review    = data['size_review']
        product_detail = ProductDetail.objects.get(id=data['product_detail_id']).id
        user_id        = data['user_id']
        image_url      = data.get('image_url',None)


        Review.objects.create(
            rating         = rating,
            comment        = comment,
            color_review   = color_review,
            size_review    = size_review,
            product_detail = product_detail,
            user_id        = user_id
            )

        review = Review.objects.get(user_id=user_id, product_detail=product_detail)

        ReviewPhoto.objects.create(
                 image_url = image_url,
                 review    = review,
                 )
        return JsonResponse({'message':'REVIEW_POSTED'},status=200)


    def get(self,request,product_id):
        target_products = ProductDetail.objects.filter(product_id=product_id)
        size_review_options  = ['small', 'good', 'big']
        color_review_options = ['bad', 'so-so', 'nice']

        review_list = []
        for target_product in target_products:
            for review in target_product.review_set.all():
                
                data={
                    'rating'      : review.rating,
                    'comment'     : review.comment,
                    'color_review': color_review_options[review.color_review],
                    'size_review' : size_review_options[review.size_review],
                    'create_at'   : review.create_at,
                    'update_at'   : review.update_at,
                    'color'       : review.product_detail.product.color.name,
                    'size'        : review.product_detail.size.name,
                    'user_id'     : review.user_id.account,
                    'image'       : [image.image_url for image in review.reviewphoto_set.all()]
                }

                review_list.append(data)

        return JsonResponse({'data': review_list}, status=200)

                  

