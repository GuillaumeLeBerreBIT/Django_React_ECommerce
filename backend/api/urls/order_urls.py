

from django.urls import path
from api.views import order_views as views

urlpatterns = [
    path('add/', views.OrderItemsAPI.as_view(), name='orders-add'),
    path('<str:pk>/', views.OrderIdAPI.as_view(), name='user-order'),
]