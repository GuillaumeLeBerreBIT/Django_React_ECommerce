
from django.urls import path
from api.views import user_views as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser.as_view(), name='register'),
    # path('', views.GetRoutes.as_view(), name='get_routes'),
    path('profile/', views.GetUserProfile.as_view(), name='get_user_profile'),
    path('profile/update/', views.UpdateUserProfile.as_view(), name='update_user_profile'),
    path('', views.GetUsers.as_view(), name='get_users'),
    path('<str:pk>/', views.UserAPI.as_view(), name='user-crud'),
    path('update/<str:pk>/', views.UpdateUser.as_view(), name='user-update'),

]