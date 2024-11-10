import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        if books:
            print(f"Books by {author_name}:")
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found for author {author_name}.")
    except Author.DoesNotExist:
        print(f"Author {author_name} not found.")

def query_books_in_library(library_name):
    """List all books in a specific library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        if books:
            print(f"Books in {library_name}:")
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found in library {library_name}.")
    except Library.DoesNotExist:
        print(f"Library {library_name} not found.")

def query_librarian_for_library(library_name):
    """Retrieve the librarian for a specific library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"The librarian for {library_name} is: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library {library_name} not found.")
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}.")

if __name__ == "__main__":
    # Example queries:
    author_name = input("Enter the author's name: ")
    query_books_by_author(author_name)

    library_name = input("Enter the library name: ")
    query_books_in_library(library_name)
    query_librarian_for_library(library_name)
