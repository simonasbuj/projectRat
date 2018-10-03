from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def fundbook(request):
    return render(request, 'entertainment/fundbook.html')

def addwish(request):
    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST.get("bookName")
        writers = request.POST.getlist("writers")
        releaseDate = request.POST.get('releaseDate')
        publisher = request.POST.get('publisher')
        description = request.POST.get('newWishComment')

        response = "TITLE: " + title +"<br>RASYTOJAI: "
        writer_lastname = ""
        for writer in writers:
            writer = writer.split()
            writer_name = writer[0]
            for word in writer[1:]:
                writer_lastname += word + ' '

        response += "vardas: " + writer_name + " pavarde: " + writer_lastname.strip()

        response += "<br>RELEASE DATE: " + str(releaseDate)
        response += "<br>PUBLISHER: " + str(publisher)
        response += "<br>COMMENT: " + description
        return HttpResponse(response)
    else:
        return HttpResponse("nepaeis")

    