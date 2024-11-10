from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', list_books, name='list_books'),  # Function-based view URL
    path('library/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view URL
]