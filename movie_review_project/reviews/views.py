from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import filters
# Reviews Views
class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({'error': 'You can only update your own reviews.'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({'error': 'You can only delete your own reviews.'}, status=403)
        return super().destroy(request, *args, **kwargs)

# User Views
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie_title', 'rating']
    ordering_fields = ['created_at', 'rating']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
