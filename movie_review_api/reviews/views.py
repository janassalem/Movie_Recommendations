from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, permissions, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.contrib.auth import logout
from django.shortcuts import redirect

from .models import Review
from .serializers import ReviewSerializer, UserSerializer
from .forms import UserRegistrationForm

# Custom pagination for reviews
class ReviewPagination(PageNumberPagination):
    page_size = 5  # Display 5 reviews per page

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie_title', 'rating']
    ordering_fields = ['rating', 'created_at']
    pagination_class = ReviewPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by movie title if specified
        movie_title = self.request.query_params.get('movie_title')
        if movie_title:
            queryset = queryset.filter(movie_title__icontains=movie_title)
        
        # Sort by rating or created date if specified
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'rating':
            queryset = queryset.order_by('-rating')
        elif sort_by == 'date':
            queryset = queryset.order_by('-created_at')

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

def home(request):
    search_query = request.GET.get('search', '')
    reviews = Review.objects.filter(movie_title__icontains=search_query) if search_query else Review.objects.all()
    return render(request, 'home.html', {'reviews': reviews})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def add_review(request):
    if request.method == 'POST':
        Review.objects.create(
            user=request.user,
            movie_title=request.POST['movie_title'],
            review_content=request.POST['review_content'],
            rating=request.POST['rating'],
        )
        return redirect('home')
    return render(request, 'add_review.html')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
