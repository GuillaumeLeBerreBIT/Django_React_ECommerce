from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .products import products
from .models import Product
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

class GetRoutes(APIView):

    def get(self, request):
        routes = [
            'GET /api/products',
            'GET /api/products/<id>',
        ]
        return Response(routes)



