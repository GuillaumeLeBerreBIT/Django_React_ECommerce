
from django.urls import path
from api.views import product_views as views

urlpatterns = [
    path('', views.GetProducts.as_view(), name='get_products'),
    path('create/', views.CreateProduct.as_view(), name='create_product'),
    path('upload/', views.UploadImage.as_view(), name='image_upload'),
    path('<str:pk>', views.GetProduct.as_view(), name='user_order'),
    path('update/<str:pk>/', views.UpdateProduct.as_view(), name='update_product'),
    path('delete/<str:pk>/', views.DeleteProduct.as_view(), name='delete_product'),
]