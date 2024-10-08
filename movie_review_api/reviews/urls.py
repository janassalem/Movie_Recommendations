from django.urls import path
from .views import ReviewListCreateView, ReviewDetailView, UserCreateView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home, add_review ,user_login, register 
from . import views
urlpatterns = [
    path('', home, name='home'),  # Home page
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    # path('add-review/', add_review, name='add_review'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),  # Optional
    # path('review/<int:review_id>/edit/', views.review_edit, name='review-edit'),
    
]



urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
