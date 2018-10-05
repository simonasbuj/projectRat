from django.shortcuts import render, redirect
from library.models import Writer
from .models import Wish

from django.utils.text import slugify
from datetime import timedelta
from django.utils import timezone

#pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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

    