from django.urls import path
from .views import ReviewListCreate, ReviewDetail, UserCreate, UserList

urlpatterns = [
    path('reviews/', ReviewListCreate.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('users/', UserCreate.as_view(), name='user-create'),
    path('users/list/', UserList.as_view(), name='user-list'),
]
