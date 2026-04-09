from rest_framework.views import APIView
from rest_framework.response import Response
from .products import products


class GetRoutes(APIView):

    def get(self, request):
        routes = [
            'GET /api/products',
            'GET /api/products/<id>',
        ]
        return Response(routes)
    
    
class GetProducts(APIView):
    
    def get(self, request):
        
        return Response(products)
    
    
class GetProduct(APIView):
    
    def get(self, request, pk):
        try:
            product = [p for p in products if p['_id'] == pk][0]
        except IndexError as e:
            product = None
            
        return Response(product)