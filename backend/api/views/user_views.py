from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..products import products
from ..models import Product
from ..serializers import ProductSerializer, UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status


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


class registerUser(APIView):

    def post(self, request):

        try:
            data = request.data

            user = User.objects.create(
                first_name=data['name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password']),
            )

            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'User with this email already exists'}
            return Response(message, status.HTTP_400_BAD_REQUEST)


class UpdateUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):

        user = request.user
        
        data = request.data 
        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        
        if data['password'] != '':
            user.password = make_password(data['password'])
        
        user.save()
        
        serializer = UserSerializerWithToken(user, many=False)
        
        return Response(serializer.data)
    
class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class GetUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, _request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class UserAPI(APIView):
    
    permission_classes = [IsAdminUser]
    
    def get(self, _request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
    def delete(self, _request, pk):
        user_for_deletion = User.objects.get(id=pk)
        user_for_deletion.delete()
        
        return Response('User was deleted')
    
class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        
        user = User.objects.get(id=pk)
        
        data = request.data 
        
        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        user.is_staff = data['isAdmin']
        
       
        user.save()
        
        serializer = UserSerializer(user, many=False)
        
        return Response(serializer.data)