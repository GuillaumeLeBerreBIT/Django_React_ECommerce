from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..products import products
from ..models import Product, Review
from ..serializers import ProductSerializer

from django.contrib.auth.hashers import make_password
from rest_framework import status


class GetProducts(APIView):

    def get(self, request):

        products = Product.objects.all()
        # Need to serialize to return real JSON data after retrieving all Queryset Objects
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


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
        data = request.data
        
        already_exists = product.review_set.filter(user=user).exists()
        
        if already_exists:
            content = {'details': 'Product already rewieved'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
        elif data['rating'] == 0:
            content = {'details': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                name=user.first_name,
                rating=data['rating'],
                comment=data['comment'],
            )
            
            reviews = product.review_set.all()
            product.numReviews = len(reviews)
            
            total = 0
            for i in reviews:
                total += i.rating 
                
            product.rating = total / len(reviews)
            product.save()
            
            return Response('Review added')