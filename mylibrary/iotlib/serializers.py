from iotlib.models import Book, Shelf
from rest_framework.serializers import ModelSerializer

class ShelfSerializer(ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['row', 'col', 'current_book', 'shelf_status']

class BookSerialzer(ModelSerializer):
    class Meta:
        model = Book
        fields = [
                'author',
                'title',
                'publisher',
                'language',
                'picture_path',
                'status',
                'history',
                'registered_date',
                'modified_date',
                ]
