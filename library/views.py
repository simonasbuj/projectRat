from django.shortcuts import render
from datetime import datetime

from .models import Book, Category

# Create your views here.

def index(request):
    selected_categories = Category.objects.filter(id__in=request.POST.getlist('Cat'))
    if request.method == 'POST' and selected_categories and 'submit_form_filter' in request.POST:
        books = Book.objects.filter(category__in=selected_categories)
    else:
        books = Book.objects.all()

    categories = Category.objects.all()
    context = {
        'books': books,
        'categories': categories,
        'selected_categories': selected_categories,
    }
    return render(request, 'library/index.html', context)

def book_details(request, slug):
    book = Book.objects.get(slug=slug)
    context = {
        'book': book,
    }
    return render(request, 'library/book_details.html', context)

def test(request):
    book_list = Book.objects.all()
    context = {
        'book_list': book_list,
    }    
    return render(request, 'library/test.html', context)