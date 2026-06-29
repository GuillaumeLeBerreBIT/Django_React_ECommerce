from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..products import products
from ..models import Product, Review
from ..serializers import ProductSerializer, ReviewSerializer

from django.contrib.auth.hashers import make_password
from rest_framework import status


class GetProducts(APIView):

    def get(self, request):
        q = request.query_params.get('keyword')
        print(q)
        
        if q == None:
            q = ''
            
        # Order explicitly so pagination boundaries are stable across requests.
        # Without .order_by(), the DB may return rows in any order, causing
        # products to repeat across pages or get skipped (UnorderedObjectListWarning).
        products = Product.objects.filter(name__icontains=q).order_by('-createdAt')
        
        page = request.query_params.get('page')
        paginator = Paginator(products, 5)
        
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        # products.number is the page the paginator actually resolved to —
        # always a valid int, even when 'page' came in empty or out of range.
        page = products.number

        # Need to serialize to return real JSON data after retrieving all Queryset Objects
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


class GetProduct(APIView):

    def get(self, request, pk):
        # try:
        #     product = [p for p in products if p['_id'] == pk][0]
        # except IndexError as e:
        #     product = None

        product = Product.objects.get(_id=pk)
        serializer = ProductSerializer(product, many=False)

        return Response(serializer.data)
    
class DeleteProduct(APIView):
    
    permission_classes = [IsAdminUser]
    
    def delete (self, request, pk):
        product = Product.objects.get(_id=pk)
        product.delete()
        return Response('Product Deteleted')
        
class CreateProduct(APIView): 
    
    permission_classes = [IsAdminUser]
    
    def post(self, request): 
        
        user = request.user
        
        product = Product.objects.create(
            user=user,
            name='Sample Name',
            price=0,
            brand='Sample Brand',
            countInStock=0,
            category='Sample Category',
            description=''
        )
        
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
        
        
class UpdateProduct(APIView):
    
    permissiom_classes = [IsAdminUser]
    
    def put(self, request, pk):
        
        data = request.data
        
        product = Product.objects.get(_id=pk)
        
        product.name = data['name']
        product.price = data['price']
        product.brand = data['brand']
        product.countInStock = data['countInStock']
        product.category = data['category']
        product.description = data['description']
        
        product.save()
        
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    
class UploadImage(APIView):
    
    def post(self, request):
        
        data = request.data
        
        product_id = data['product_id']
        product = Product.objects.get(_id=product_id)
        
        product.image = request.FILES.get('image')
        product.save()

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    
class CreateProductReview(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        user = request.user
        product = Product.objects.get(_id=pk)
        
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.validated_data['rating']
        comment = serializer.validated_data.get('comment', '')
        
        already_exists = product.review_set.filter(user=user).exists()
        
        if already_exists:
            content = {'detail': 'Product already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
        elif rating == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                name=user.first_name,
                rating=rating,
                comment=comment,
            )
            
            reviews = product.review_set.all()
            product.numReviews = len(reviews)
            
            total = 0
            for i in reviews:
                total += i.rating 
                
            product.rating = total / len(reviews)
            product.save()
            
            return Response('Review added')