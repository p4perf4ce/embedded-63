from django.db.models import fields
from rest_framework import serializers
from iotlib.models import Book, Shelf
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer


class BookStateSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title',
            'status',
            'modified_date'
        ]

class ShelfInfoSerializer(ModelSerializer):
    current_book = BookStateSerializer(read_only=True)
    class Meta:
        model = Shelf
        fields = ['row', 'col', 'current_book']

class ShelfStateSerializer(ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['row', 'col', 'shelf_status']

class BookSerialzer(ModelSerializer):
    class Meta:
        model = Book
        fields = [
                'author',
                'title',
                'publisher',
                'language',
                'picture',
                'status',
                'history',
                'registered_date',
                'modified_date',
                ]
