from django.contrib import admin
from .models import Book

# Register the Book model with the admin site
admin.site.register(Book)
admin.ModelAdmin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)