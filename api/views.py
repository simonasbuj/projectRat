from django.shortcuts import render
from rest_framework import viewsets
from library.models import Book
from .serializers import BookSerializer

# Create your views here.
class BookView(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get']        
