from django.contrib import admin
from .models import Book, Writer, Tag, Category, BookTags
# Register your models here.

admin.site.register(Book)
admin.site.register(Writer)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(BookTags)
