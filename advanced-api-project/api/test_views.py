from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book, Author

class BookTests(APITestCase):

    def setUp(self):
        """Create initial test data for books and authors."""
        # Create author
        self.author = Author.objects.create(name="J.K. Rowling")
        
        # Create some books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone", 
            publication_year=1997,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets", 
            publication_year=1998,
            author=self.author
        )
        
        # Create a user for testing authentication
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_create_book(self):
        """Test the creation of a new book."""
        url = "/books/"
        data = {
            "title": "Harry Potter and the Prisoner of Azkaban",
            "publication_year": 1999,
            "author": self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_read_book_list(self):
        """Test retrieving the list of books."""
        url = "/books/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We should have 2 books in the database

    def test_read_single_book(self):
        """Test retrieving a single book by ID."""
        url = f"/books/{self.book1.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_update_book(self):
        """Test updating an existing book."""
        url = f"/books/{self.book1.id}/"
        data = {
            "title": "Harry Potter and the Philosopher's Stone (Updated)",
            "publication_year": 1997,
            "author": self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()  # Refresh the book instance from the database
        self.assertEqual(self.book1.title, "Harry Potter and the Philosopher's Stone (Updated)")

    def test_delete_book(self):
        """Test deleting a book."""
        url = f"/books/{self.book1.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # Only 1 book should remain

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        url = "/books/?title=Harry Potter"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both books should be returned

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        url = f"/books/?author={self.author.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both books by the author

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        url = "/books/?publication_year=1997"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 book should be returned

    def test_search_books(self):
        """Test searching books by title or author."""
        url = "/books/?search=Chamber"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 book contains "Chamber" in the title

    def test_order_books_by_title(self):
        """Test ordering books by title."""
        url = "/books/?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # The list should be sorted by title

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year."""
        url = "/books/?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))  # The list should be sorted by publication year

    def test_permissions_for_create_book(self):
        """Test that only authenticated users can create a book."""
        self.client.logout()  # Log out to test unauthorized access
        url = "/books/"
        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Unauthorized
