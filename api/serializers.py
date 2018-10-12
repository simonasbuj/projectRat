from rest_framework import serializers
from library.models import Book, Writer
from entertainment.models import Wish
from accounts.models import Info
from django.contrib.auth.models import User


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


class UserSerializer(serializers.ModelSerializer):
    # avatar_url = serializers.CharField(read_only=True)
    profile_picture = serializers.CharField(source='info.avatar_url', read_only=True)
    class Meta:
        model = User
        fields = ('username', 'profile_picture')


class WishSerializer(serializers.ModelSerializer):
    #many to many fields
    writers = WriterSerializer(many=True, read_only=True)

    created_by = UserSerializer()

    #custom fields from model class
    donated = serializers.DecimalField(max_digits=5, decimal_places=2, source='get_transaction_sum', read_only=True)
    days_left = serializers.CharField(source='get_timeleft', read_only=True)
    api_url = serializers.CharField(read_only=True)

    class Meta:
        model = Wish
        fields = ('id', 'title', 'description', 'price', 'donated', 'days_left', 'status', 'writers', 'api_url', 'created_by')
