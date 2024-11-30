from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List view
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Detail view
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Create view
    path('books/update/', BookUpdateView.as_view(), name='book-update'),  # Update view
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),  # Delete view
]
