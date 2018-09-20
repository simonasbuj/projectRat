from django.shortcuts import render
from rest_framework import viewsets, generics, filters
from library.models import Book
from .serializers import BookSerializer

# Create your views here.
class BookView(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get']

class SearchBooksView(generics.ListAPIView):

    serializer_class = BookSerializer

    def get_queryset(self):
        keyword = self.kwargs['keyword']
        return Book.objects.filter(slug__icontains=keyword.replace(" ", "-"))