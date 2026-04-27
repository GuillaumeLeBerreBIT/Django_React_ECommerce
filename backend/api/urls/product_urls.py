
from django.urls import path
from api.views import product_views as views

urlpatterns = [
    path('', views.GetProducts.as_view(), name='get_products'),
    path('<str:pk>', views.GetProduct.as_view(), name='get_product'),
]