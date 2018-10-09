from django.shortcuts import render, redirect, get_object_or_404
from library.models import Writer
from .models import Wish, Transaction

from django.utils.text import slugify
from datetime import timedelta
from django.utils import timezone

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
