from rest_framework import serializers
from library.models import Book, Writer
from entertainment.models import Wish


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ('id', 'name', 'last_name')

class BookSerializer(serializers.ModelSerializer):
    writers = WriterSerializer(many=True, read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'cover', 'writers', 'url', 'cover_url')


class WishSerializer(serializers.ModelSerializer):
    #many to many fields
    writers = WriterSerializer(many=True, read_only=True)

    #custom fields from model class
    donated = serializers.DecimalField(max_digits=5, decimal_places=2, source='get_transaction_sum', read_only=True)
    days_left = serializers.CharField(source='get_timeleft', read_only=True)
    api_url = serializers.CharField(read_only=True)

    class Meta:
        model = Wish
        fields = ('id', 'title', 'description', 'price', 'donated', 'days_left', 'status', 'writers', 'api_url')