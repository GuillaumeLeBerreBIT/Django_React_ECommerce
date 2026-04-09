from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetRoutes.as_view(), name='get_routes'),
    path('products/', views.GetProducts.as_view(), name='get_products'),
    path('products/<str:pk>', views.GetProduct.as_view(), name='get_product'),
]