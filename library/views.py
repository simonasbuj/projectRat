from django.shortcuts import render

from .models import Book

# Create your views here.

def index(request):
    return render(request, 'library/index.html')

def test(request):
    book_list = Book.objects.all()
    context = {
        'book_list': book_list,
    }
    return render(request, 'library/test.html', context)