import json

from django.http  import JsonResponse
from django.views import View
from django.db.models import Q 

from products.models import Product, ProductDetail, ProductSale, ProductSeason, Season, Size, Image, ImageClassification, Category

class BestItemView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-productsale__product_sales')
        SHOW_NUMBER = 8
        best_items=[
                {
                    'id'            : product.id,
                    'name'          : product.name,
                    'price'         : product.price,    
                    'image'         : [
                        {
                        'name'      :image.image_classification.name,
                        'image_url' : image.image_url} for image in product.image_set.all()],
                    'product_stock' : [
                        {
                        'size' :size.name,
                        'stock':ProductDetail.objects.get(size_id=size.id,product_id=product.id).stock} for size in product.size.all()],                       
                    }                        
                for product in products[:(SHOW_NUMBER-1)]]
        return JsonResponse({'best_items':best_items}, status=200)

class ProductView(View):
    def get(self, request):
        ordering           = request.GET.get('ordering', '-release_at')        
        category           = request.GET.get('category', None)
        size               = request.GET.getlist('size', None)
        color              = request.GET.getlist('color', None)
        price_upper_range  = request.GET.get('PriceUpper', 1000000)
        price_lower_range  = request.GET.get('PriceLower', 0)

        q=Q()
        if category:
            q &= Q(category_id = category)
        if color:
            q &= Q(color_name__in = color)
        if size:
            q &= Q(size__name__in = size)
        q &= Q(price__range = (int(price_lower_range),int(price_upper_range)))
        
        products = Product.objects.filter(q).order_by(ordering)
        
        page               = int(request.GET.get('PageNo',1))
        product_number     = len(products)
        showing_number     = int(request.GET.get('Show',10))        

        if page <= (product_number // showing_number):
            product_in_page = products[showing_number*(page-1) : showing_number*page]
        else:
            product_in_page = products[showing_number*(page-1) : showing_number*(page-1) + product_number % showing_number]

        product_list=[
            {
                'id'            : product.id,
                'name'          : product.name,
                'price'         : product.price,
                'image'         : [
                    {
                    'name'      :image.image_classification.name, 
                    'image_url' : image.image_url
                    } for image in product.image_set.all()],
                'product_stock' : [
                    {
                    'size'      :size.name,
                    'stock'     :ProductDetail.objects.get(size_id=size.id,product_id=product.id).stock} for size in product.size.all()]
                }
            for product in product_in_page]
        

        return JsonResponse({'category_name':Category.objects.get(id=category).name if category else None,'product_list':product_list}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_info   = [
            {
                'id'               : product.id,
                'name'             : product.name,
                'price'            : product.price,
                'image'            : [{
                    'name'         :image.image_classification.name,
                    'image_url'    : image.image_url} for image in product.image_set.all()],
                'product_stock'    : [
                    {
                    'size'         :size.name,
                    'stock'        :ProductDetail.objects.get(size_id=size.id,product_id=product.id).stock} for size in product.size.all()],
                'season'           : [season.name for season in product.season.all()],
                'color'            : [
                    {
                    'product_id'   :color_product.id,
                    'product_image':color_product.image_set.all()[0].image_url} for color_product in Product.objects.filter(name=product.name)],
                }
            ]
        return JsonResponse({'MESSAGE':'SUCCESS','product_info': product_info}, status=200)