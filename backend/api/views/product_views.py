from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..products import products
from ..models import Product
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
