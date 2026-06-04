from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..products import products
from ..models import Product, Order, OrderItem, ShippingAddress
from ..serializers import ProductSerializer, OrderSerializer

from django.contrib.auth.hashers import make_password
from rest_framework import status


class OrderItemsAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        data = request.data

        order_items = data['orderItems']

        if order_items and len(order_items) == 0:
            return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

        else:

            order = Order.objects.create(
                user=user,
                paymentMethod=data['paymentMethod'],
                taxPrice=data['taxPrice'],
                shippingPrice=data['shippingPrice'],
                totalPrice=data['totalPrice']
            )

            shipping = ShippingAddress.objects.create(
                order=order,
                address=data['shippingAddress']['address'],
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postalCode'],
                country=data['shippingAddress']['country'],
            )
            
            for i in order_items:
                product = Product.objects.get(_id=i['product'])
                
                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    name=product.name,
                    quantity=i['qty'],
                    price=i['price'],
                    image=product.image.url,
                )

                product.countInStock -= item.quantity
                product.save()
                
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)


class OrderIdAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        
        try:
            order = Order.objects.get(_id=pk)
            user = request.user
            
            if user.is_staff or order.user == user:
                serializer = OrderSerializer(order, many=False)
                return Response(serializer.data)
            else:
                Response({'detail': 'Not Authorized to view this order'},
                         status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'detial': 'Order does not exist.'}, status=status.HTTP_400_BAD_REQUEST)