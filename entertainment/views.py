from django.shortcuts import render, redirect, get_object_or_404
from .models import Wish, Transaction
from library.models import Book, Order, Category, Writer
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import timedelta

from django.utils.text import slugify
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone
import random
import json

#pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

#stripe
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

#for tests
from django.http import HttpResponse

# Create your views here.

def fundbook(request,  **kwargs):
    context = {}
    if 'newWishSuccess' in request.session:
        if request.session['newWishSuccess']:
            context['success'] = True
            del request.session['newWishSuccess']
        else:
            context['error'] = True
            del request.session['newWishSuccess']

    howold = timezone.now() - timedelta(days=30)
    wishes = Wish.objects.filter(updated_at__gt=howold, status='o')

    paginator = Paginator(wishes, 24) #kiek objektų viename psl
    page = request.GET.get('p')
    wishes = paginator.get_page(page)

    context['wishes'] = wishes

    return render(request, 'entertainment/fundbook.html', context)

def addwish(request):
    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST.get("bookName")
        writers = request.POST.getlist("writers")
        releaseDate = None if not request.POST.get('releaseDate') else request.POST.get('releaseDate')
        publisher =  None if not request.POST.get('publisher') else request.POST.get('publisher')
        description = request.POST.get('newWishComment')
        wish = Wish.objects.create(title=title, publish_date=releaseDate, description=description, publisher=publisher, created_by=request.user)


        for writer in writers:
            writer_lastname = ""
            try:
                writerdb = Writer.objects.get(slug=slugify(writer))
                wish.writers.add(writerdb)
            except:
                writer = writer.split()
                writer_name = writer[0]
                for word in writer[1:]:
                    writer_lastname += word + ' '
                w = Writer.objects.create(name=writer_name, last_name=writer_lastname.strip())
                wish.writers.add(w)

        request.session['newWishSuccess'] = True
        return redirect('entertainment:fundbook')
    else:
        request.session['newWishSuccess'] = False
        return redirect('entertainment:fundbook')

def payment(request):
    if request.method == 'POST':
        payerFirstName = None if not request.POST.get('payerFirstName') else request.POST.get('payerFirstName')
        payerLastName = None if not request.POST.get('payerLastName') else request.POST.get('payerLastName')
        user = None if not request.user.is_authenticated else request.user
        wish_id = request.POST.get('wish_id')
        amount = float(request.POST.get('amount'))
        stripe_token = request.POST.get('stripe_token')
        email = request.POST.get('email')

        wish = get_object_or_404(Wish, id=wish_id)

        ##charge payment and save transaction
        response = stripe.Charge.create(
            amount = int(amount * 100),
            currency = 'eur',
            source = stripe_token,
            description = "Pervedimas prašymui ID: " + str(wish.id) + " PAVADINIMAS: " + wish.title,
            receipt_email = email
        )

        Transaction.objects.create(
            charge_id = response['id'],
            amount = float(response['amount']/100),
            email = email,
            firstname = payerFirstName,
            lastname = payerLastName,
            user = user,
            wish = wish
        )

        return HttpResponse("OK<br>NORAS: " + str(wish.id) + " " + wish.title + "<br>CHARGE ID: " + response['id'] + "<br>AMOUNT: " + str(float(response['amount']/100)) + " EUR<br>EMAIL: " + email)
    else:
        return redirect('entertainment:fundbook')


def tinder(request):

    if not request.user.is_authenticated:
        return redirect('library:index')

    #get relevant data, like genres, tags, writers of the books that user read.
    orders = Order.objects.filter(user = request.user).exclude(status = 'o')

    # 1 budas
    # read_books = Book.objects.none()
    # for o in orders:
    #     read_books |= o.books.all()
    # read_books = read_books.distinct()
    # print(read_books)

    # 2 budas
    # order_ids = []
    # for o in orders:
    #     order_ids.append(o.id)
    # read_books = Book.objects.filter(order__id__in=order_ids).distinct()
    # print(read_books)

    #normalus budas
    read_books = Book.objects.filter(order__in=orders).distinct()

    #get relevant categories, writers from read books
    categories = Category.objects.filter(book__in=read_books).distinct()
    writers = Writer.objects.filter(book__in=read_books).distinct()

    #get similar users
    max_age = request.user.info.birth_date + timedelta(days=1825)
    min_age = request.user.info.birth_date - timedelta(days=1825)
    similar_users = User.objects.filter(info__birth_date__lt=max_age, info__birth_date__gt=min_age).exclude(id=request.user.id)

    # 'su' stands for similar users
    su_orders = Order.objects.filter(user__in = similar_users).exclude(status = 'o')
    su_books = Book.objects.filter(order__in=su_orders).distinct()
    su_categories = Category.objects.filter(book__in=su_books).distinct()
    su_writers = Writer.objects.filter(book__in=su_books).distinct()
    print(su_books)
    print(su_categories)
    print(su_writers)

    #monster query ... Q objects, creates a query. '|' means 'or', '&' means 'and' '~' before Q means 'not'
    books = Book.objects.filter((Q(category__in=categories) |  Q(writers__in=writers)
                                | Q(category__in=su_categories) | Q(writers__in=su_writers) | Q(id__in = su_books)
                                )
                                & ~Q(id__in = read_books)
                                & ~Q(id__in = request.user.info.bookmarks.all())
                                & ~Q(id__in = request.user.info.book_dislikes.all())
                                & ~Q(id=request.session.get('last_offered_book', 0))
                                ).distinct()

    if not books:
        request.session['last_offered_book'] = 0
        return render(request, 'entertainment/tinder.html')

    max_num = books.count() - 1
    random_num = random.randint(0,max_num)
    book = books[random_num]
    request.session['last_offered_book'] = book.id
    #tell user why the book was selected
    reasons = []
    if book.category in categories:
        reasons.append('Skaitėte knygas, kurių žanras yra <b>' + str(book.category) + '</b>')
    for w in book.writers.all():
        if w in writers:
            reasons.append('Skaitėte kitas <b>' + str(w) + '</b> knygas')
        if w in su_writers:
            reasons.append('Jūsų bendraamžiai skaito <b>' + str(w) + '</b> knygas')
    if book.category in su_categories:
        reasons.append('Jūsų bendraamžiai skaito <b>' + str(book.category) + '</b> žanro knygas')
    if book in su_books:
        reasons.append('Jūsų bendraamžiai skaitė šią knygą')


    random.shuffle(reasons)
    context = {
        'book': book,
        'reasons': reasons
    }

    return render(request, 'entertainment/tinder.html', context)


def like_book(request):
    if request.method == "POST" and request.user.is_authenticated:
        json_data = json.loads(request.body)
        book = get_object_or_404(Book, id=json_data['bookId'])
        request.user.info.bookmarks.add(book)
        return HttpResponse("Ok")
    else:
        return redirect('library:index')


def dislike_book(request):
    if request.method == "POST" and request.user.is_authenticated:
        json_data = json.loads(request.body)
        book = get_object_or_404(Book, id=json_data['bookId'])
        request.user.info.book_dislikes.add(book)
        return HttpResponse("Ok")
    else:
        return redirect('library:index')


def addbook(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return redirect('library:index')

    title = request.POST.get('bookName')
    writers = request.POST.getlist("writers")
    description = request.POST.get('bookDescription')
    category = Category.objects.get(id=request.POST.get("newBookCategory"))
    owner = request.user
    cover = None if not request.FILES.get('newBookCover') else request.FILES.get('newBookCover')

    book = Book.objects.create(title=title, description=description, category=category, owner=owner, cover=cover)

    for writer in writers:
        writer_lastname = ""
        try:
            writerdb = Writer.objects.get(slug=slugify(writer))
            book.writers.add(writerdb)
        except:
            writer = writer.split()
            writer_name = writer[0]
            for word in writer[1:]:
                writer_lastname += word + ' '
            w = Writer.objects.create(name=writer_name, last_name=writer_lastname.strip())
            book.writers.add(w)


    return redirect('library:index')

def deletebook(request, id):
    book = get_object_or_404(Book, id=id)

    if book.owner == request.user:
        book.delete()
        return redirect('library:index')
    else:
        return redirect('library:book_details', slug=book.slug)
