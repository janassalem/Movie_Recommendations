from django.urls import path
from .views import (
    ReviewListCreateView,
    ReviewDetailView,
    UserCreateView,
    UserDetailView,
    home,
    add_review,
    user_login,
    user_logout,  # Add logout view import
    register,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),  # Add logout path
    path('register/', register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
