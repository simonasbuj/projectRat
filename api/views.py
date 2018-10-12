from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from library.models import Book
from entertainment.models import Wish
from .serializers import BookSerializer, WishSerializer
from unidecode import unidecode

# Create your views here.
class BookView(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get']

class SearchBooksView(generics.ListAPIView):

    serializer_class = BookSerializer

    def get_queryset(self):
        keyword = self.kwargs['keyword']
        keyword = unidecode(keyword.strip())
        return Book.objects.filter(slug__icontains=keyword.replace(" ", "-"))


class WishView(viewsets.ViewSet):

    def list(self, request):
        queryset = Wish.objects.filter(status='o')
        serializer = WishSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Wish.objects.filter(status='o')
        wish = get_object_or_404(queryset, pk=pk)
        serializer = WishSerializer(wish)
        return Response(serializer.data)

    # add post request
    """ def create(self, request):
        pass """
