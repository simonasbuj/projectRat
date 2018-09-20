from django.shortcuts import render

# Create your views here.

def fundbook(request):
    return render(request, 'entertainment/fundbook.html')
    