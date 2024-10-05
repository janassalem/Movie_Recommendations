from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from .models import Review
from .serializers import ReviewSerializer, UserSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django import forms
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .forms import UserRegistrationForm

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

# class MovieReviewListView(generics.ListAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     pagination_class = ReviewPagination
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ['movie_title']
#     ordering_fields = ['rating', 'created_at']
#     ordering = ['-created_at']

#     def get_queryset(self):
#         movie_title = self.request.query_params.get('movie_title', None)
#         if movie_title is None:
#             raise ValidationError({"movie_title": "This field is required."}, code=status.HTTP_400_BAD_REQUEST)
#         return Review.objects.filter(movie_title__iexact=movie_title)

#     def handle_exception(self, exc):
#         response = super().handle_exception(exc)
#         if isinstance(exc, ValidationError):
#             response.data = {'error': response.data}
#         return response
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

def home(request):
    search_query = request.GET.get('search', '')
    if search_query:
        reviews = Review.objects.filter(movie_title__icontains=search_query)
    else:
        reviews = Review.objects.all()
    
    return render(request, 'home.html', {'reviews': reviews})
    reviews = Review.objects.all()
    return render(request, 'home.html', {'reviews': reviews})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@login_required
def add_review(request):
    if request.method == 'POST':
        movie_title = request.POST['movie_title']
        review_content = request.POST['review_content']
        rating = request.POST['rating']
        Review.objects.create(
            user=request.user,
            movie_title=movie_title,
            review_content=review_content,
            rating=rating,
        )
        return redirect('home')  # Redirect to home after adding a review
    return render(request, 'add_review.html')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})





class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        # Get the review or return 404 if not found
        review = get_object_or_404(Review, pk=self.kwargs.get('pk'))
        return review




