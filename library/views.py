#testing
from django.shortcuts import redirect

from django.shortcuts import render, get_object_or_404, render_to_response
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone

#ajax
from django.core import serializers
from django.forms.models import model_to_dict
import json

#pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

#difficult queries (or)
from django.db.models import Q
from unidecode import unidecode #lietuviskas raides pakeicia i angliskas, del paieskos

#models
from .models import Book, Category, Order
from accounts.models import Comment

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
    paginator = Paginator(books, 9) #kiek objektų viename psl
    page = request.GET.get('p')
    books = paginator.get_page(page)
    context = {
        'books': books,
        'categories': categories,
        'selected_categories': selected_categories,
    }
    return render(request, 'library/index.html', context)

def book_details(request, slug, id):
    #book = Book.objects.get(slug=slug)
    book = get_object_or_404(Book, slug=slug, id=id)
    similar_books = Book.objects.filter((Q(category=book.category) |  Q(tags__in=book.tags.all())) & ~Q(id = book.id)).distinct()[:24]
    #print(similar_books[4])
    max_num_of_replies = 5

    start_date = timezone.now().date()
    future_dates = []
    for single_date in (start_date + timedelta(n) for n in range(14)):
        future_dates.append(single_date)

    orders = book.order_set.all().exclude(status='s')
    lb_order = book.order_set.last()
    lu_order = None
    if request.user.is_authenticated:
        lu_order = request.user.order_set.last()

    cant_order = ''
    if request.user.is_authenticated and lu_order and lu_order.status == 'r':
        cant_order = 'PRAŠOM GRĄŽINTI KNYGĄ <a class="text-dark font-weight-bold" href="/knyga/' + lu_order.books.last().slug + '-' + str(lu_order.books.last().id) + '">' + lu_order.books.last().title + '</a> (nuo: ' + str(lu_order.take_date) + ' iki: ' + str(lu_order.return_date) + ')'
    elif request.user.is_authenticated and lu_order and lu_order.status != 's':
        cant_order = 'Jau rezervavai <a class="text-dark font-weight-bold" href="/knyga/' + lu_order.books.last().slug + '-' + str(lu_order.books.last().id) + '">' + lu_order.books.last().title + '</a> (nuo: ' + str(lu_order.take_date) + ' iki: ' + str(lu_order.return_date) + ')'
    elif lb_order and (lb_order.status == 't' or lb_order.status == 'r'):
        cant_order = 'Knygą rezervavo kitas narys. Ši knyga bus prieinama nuo ' + str(lb_order.return_date)
    context = {
        'book': book,
        'max_num_of_replies': max_num_of_replies,
        'similar_books': similar_books,
        'start_date': start_date,
        'future_dates': future_dates,
        'orders': orders,
        'cant_order': cant_order
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

def reservation(request, slug, id):
    if not request.user.is_authenticated or not request.method == "POST":
        return redirect('library:index')

    book = get_object_or_404(Book, slug=slug, id=id)
    take_date = request.POST.get('take_date')
    return_date = request.POST.get('return_date')

    new_order = Order.objects.create(user=request.user, take_date=take_date, return_date=return_date)
    new_order.books.add(book)
    return HttpResponse(str(new_order))

def reservation_answer(request, id):
    order = get_object_or_404(Order, id=id)
    book = order.books.last()
    if request.user != book.owner or request.method != 'POST':
        return redirect('library:index')

    if request.POST.get('okBtn'):
        order.status = 't'
        order.save()
        for o in book.order_set.all():
            if o.status == 'o':
                o.delete()
        return redirect('library:book_details', slug=book.slug, id=book.id)
    elif request.POST.get('cancelBtn'):
        order.delete()
        return redirect('library:book_details', slug=book.slug, id=book.id)
    elif request.POST.get('returnedBtn'):
        order.status = 's'
        order.save()
        return redirect('library:book_details', slug=book.slug, id=book.id)
    elif request.POST.get('reportBtn'):
        order.status = 'r'
        order.save()
        return redirect('library:book_details', slug=book.slug, id=book.id)

    return HttpResponse("neveikia...")

#norender
def bookmark(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.is_ajax():
        if request.user.is_authenticated:
            if book in request.user.info.bookmarks.all():
                #remove from bookmarks
                request.user.info.bookmarks.remove(book)
            else:
                #add to bookmarks
                request.user.info.bookmarks.add(book)

            data = {'success': True}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('Neprisijungęs', status=401)
    else:
        return redirect(book)

def comment(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        parent_id = int(request.POST.get("parentId"))
        text = request.POST.get("text")
        #empty comment
        if not text:
            data = {
                'error': "negali buti tuscias"
            }
            return JsonResponse(data)
        #comment without parent
        if parent_id == 0:
            comment = Comment.objects.create(text=text, created_by=user, book=book)

            if book.comment_set.all().count() <= 1:
                no_comments = 1
            else:
                no_comments = 0
            data = {
                'id': comment.id,
                'text': comment.text,
                'created_by': comment.created_by.username,
                'no_comments': no_comments,
            }
            return JsonResponse(data)
        #comment with parent
        if parent_id > 0:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            if not parent_comment.parent:
                comment = Comment.objects.create(text=text, created_by=user, book=book, parent=parent_comment)
            else:
                original_parent_coment = parent_comment.parent
                parent_id = original_parent_coment.id
                comment = Comment.objects.create(text=text, created_by=user, book=book, parent=original_parent_coment)

            if comment.parent.replies.all().count() <= 1:
                no_comments = 1
            else:
                no_comments = 0

            data = {
                'parent_id': parent_id,
                'id': comment.id,
                'text': comment.text,
                'created_by': comment.created_by.username,
                'no_comments': no_comments,
            }
            return JsonResponse(data)


        print("bandysim addinti comment knygai: " + text + " su id: " + parent_id)
        return redirect(book)
    else:
        print("nepaeis")
        return redirect(book)

def landing(request):
    return render(request, 'library/landing.html')
