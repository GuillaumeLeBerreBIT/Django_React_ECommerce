from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.GetRoutes.as_view(), name='get_routes'),
    path('users/profile/', views.GetUserProfile.as_view(), name='get_user_profile'),
    path('users/', views.GetUsers.as_view(), name='get_users'),
    path('products/', views.GetProducts.as_view(), name='get_products'),
    path('products/<str:pk>', views.GetProduct.as_view(), name='get_product'),
]