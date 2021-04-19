import json

from django.http  import JsonResponse
from django.views import View 

from products.models import *

class ProductCategoryView(View):
    def get(self, request):
        ordering_id        = request.GET.get('ordering', 0)
        category           = request.GET.get('category', None)
        size               = request.GET.get('size', None)
        page               = request.GET.get('PageNo',1)
        
        if category:
            products       = Product.objects.filter(category_id=category)
        else:
            products       = Product.objects.all()
        
        product_number     = len(products)
        showing_number     = request.GET.get('Show',10)
        
        ReleaseDateOrder   = products.order_by('-release_at')
        PriceOrderHigh     = products.order_by('-price')
        PriceOrderLow      = products.order_by('price')       
        ProductSalesOrder  = products.order_by('-productsale__product_sales')

        ordering_list = [ReleaseDateOrder,PriceOrderHigh,PriceOrderLow,ProductSalesOrder]   
        best_items    = []
        product_list  = []

        if category==None:
            for product in ProductSalesOrder:
                product_images = [{'name':image.image_classification.name, 'image_url' : image.image_url} for image in product.image_set.all()]
                product_stocks = [{'size':size.name,'stock':ProductDetail.objects.get(size_id=size.id,product_id=product.id).stock} for size in product.size.all()]
                best_items.append(
                    {
                        'id'            : product.id,
                        'name'          : product.name,
                        'price'         : product.price,
                        'image'         : product_images,
                        'product_stock' : product_stocks,                       
                        }                        
                    )

        if page <= (product_number // showing_number):
            product_in_page = ordering_list[ordering_id][showing_number*(page-1) : showing_number*page]
        else:
            product_in_page = ordering_list[ordering_id][showing_number*(page-1) : showing_number*(page-1) + product_number % showing_number]

        for product in product_in_page:
            product_images = [{'name':image.image_classification.name, 'image_url' : image.image_url} for image in product.image_set.all()]
            product_stocks = [{'size':size.name,'stock':ProductDetail.objects.get(size_id=size.id,product_id=product.id).stock} for size in product.size.all()]
            product_list.append(
                {
                    'id'            : product.id,
                    'name'          : product.name,
                    'price'         : product.price,
                    'image'         : product_images,
                    'product_stock' : product_stocks,  
                    }
                )
        if category:
            return JsonResponse({'category_name':Category.objects.get(id=category).name,'product_list':product_list}, status=200)
        return JsonResponse({'best_itmes':best_items,'product_list':product_list}, status=200)

class ProductView(View):
    def get(self, request, product_id):

        product = Product.objects.filter(id=product_id)[0]
        product_info = []
        product_seasons = [season.name for season in product.season.all()]
        product_images = [{'name':image.image_classification.name, 'image_url' : image.image_url} for image in product.image_set.all()]
        product_stocks = [{'size':size.name,'stock':ProductDetail.objects.get(size_id=size.id,product_id=product.id).stock} for size in product.size.all()]
        product_colors = [{'product_id':color_product.id,'product_image':color_product.image_set.all()[0].image_url} for color_product in Product.objects.filter(name=product.name)]
        product_info.append(
            {
                'id'            : product.id,
                'name'          : product.name,
                'price'         : product.price,
                'image'         : product_images,
                'product_stock' : product_stocks,
                'season'        : product_seasons,
                'color'         : product_colors,
                }
            )
        return JsonResponse({'product_info': product_info}, status=200)