from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .products import products
from .models import Product
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'Hello World'
    #     # ...

    #     return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
    
        serializer = UserSerializerWithToken(self.user).data
        
        for k, v in serializer.items():
            data[k] = v
        
        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class GetRoutes(APIView):

    def get(self, request):
        routes = [
            'GET /api/products',
            'GET /api/products/<id>',
        ]
        return Response(routes)
    

class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    
class GetUsers(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data)
    
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