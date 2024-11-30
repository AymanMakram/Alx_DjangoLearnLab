from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter

# Filter class for Book model
class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')  # Allows partial match for title
    author = filters.CharFilter(lookup_expr='icontains')  # Allows partial match for author
    publication_year = filters.NumberFilter()  # Exact match for publication_year
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']




class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter, filters.OrderingFilter)
    filterset_class = BookFilter
    search_fields = ['title', 'author']  # Enable search on title and author
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access

# Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only

# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only

# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users only
