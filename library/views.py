#testing
from django.shortcuts import redirect

from django.shortcuts import render, get_object_or_404, render_to_response
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse


#pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

#difficult queries (or)
from django.db.models import Q
from unidecode import unidecode #lietuviskas raides pakeicia i angliskas, del paieskos

#models
from .models import Book, Category

# Create your views here.

def index(request):
    selected_categories = Category.objects.filter(id__in=request.POST.getlist('Cat'))    
    if request.method == 'POST' and selected_categories and 'submit_form_filter' in request.POST:
        books = Book.objects.filter(category__in=selected_categories)
        request.session['selected_categories'] = request.POST.getlist('Cat')
        return HttpResponseRedirect(reverse('library:index'))
    elif request.method == 'POST' and not selected_categories:
        request.session['selected_categories'] = request.POST.getlist('Cat')
        books = Book.objects.all()
        return HttpResponseRedirect(reverse('library:index'))
    elif request.session.get('selected_categories',0):
        selected_categories = Category.objects.filter(id__in=request.session['selected_categories'])
        books = Book.objects.filter(category__in=selected_categories)    
    else:
        books = Book.objects.all()

    categories = Category.objects.all()
    paginator = Paginator(books, 24) #kiek objektų viename psl
    page = request.GET.get('p')
    books = paginator.get_page(page)
    context = {
        'books': books,
        'categories': categories,
        'selected_categories': selected_categories,
    }
    return render(request, 'library/index.html', context)

def book_details(request, slug):
    #book = Book.objects.get(slug=slug)
    book = get_object_or_404(Book, slug=slug)
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

def search(request):
    if request.method == 'POST' and request.POST.get('keywoard'):
        keyword = request.POST.get('keywoard').strip()
        print(keyword)
        #books = Book.objects.filter(Q(slug__icontains=keyword.replace(" ", "-")) | Q(title__icontains=keyword) | Q(category__name__icontains=keyword))
        keyword = unidecode(keyword)
        books = Book.objects.filter(Q(slug__icontains=keyword.replace(" ", "-")) | Q(category__name__icontains=keyword))
        categories = Category.objects.all()
        context = {
            'books': books,
            'categories': categories,

        }
        return render(request, 'library/index.html', context)
    else:
        print('Nieko neivedei')

    return redirect('library:index')

""" def logout_view(request):
    logout(request)
    return redirect('/knygos') """
