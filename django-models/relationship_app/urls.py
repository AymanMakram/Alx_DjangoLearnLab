from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', list_books, name='list_books'),  # Function-based view URL
    path('library/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view URL
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]

