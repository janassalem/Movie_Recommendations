from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Review
from .serializers import ReviewSerializer, UserSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Custom pagination class for reviews
class ReviewPagination(PageNumberPagination):
    page_size = 5  # Display 5 reviews per page

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie_title', 'rating']
    ordering_fields = ['rating', 'created_at']
    pagination_class = PageNumberPagination
   
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by movie title
        movie_title = self.request.query_params.get('movie_title', None)
        if movie_title:
            queryset = queryset.filter(movie_title__icontains=movie_title)
        
        # Optional sorting by rating or created date
        sort_by = self.request.query_params.get('sort_by', None)
        if sort_by == 'rating':
            queryset = queryset.order_by('-rating')  # Sort by rating in descending order
        elif sort_by == 'date':
            queryset = queryset.order_by('-created_at')  # Sort by created date in descending order

        return queryset


    

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionError("You can only update your own reviews.")
        serializer.save()

class UserCreateView(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]




