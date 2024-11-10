from django.db import models
from models import Book
# Creating a Book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()