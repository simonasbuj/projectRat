from rest_framework import serializers
from library.models import Book, Writer


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ('id', 'name', 'last_name')

class BookSerializer(serializers.ModelSerializer):
    writers = WriterSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'cover', 'writers')