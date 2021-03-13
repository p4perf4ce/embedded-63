from typing import Dict
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http.request import HttpRequest
# Register your models here.

from .models import Book, Shelf

# Register views here

class BookAdmin(ModelAdmin):
    # fields = ('title', ('author', 'publisher'), 'picture_path', 'language', 'owner', 'status')
    fieldsets = (
        (
            'Book Information', {
                'fields': ('title', ('author', 'publisher'), 'picture', 'language')
            }
        ),
        (
            'Additional Information', {
                'fields': ('owner', 'status')
            }
        )
    )

    search_fields = ['title', 'author']

    list_display = ('title', 'author', 'publisher', 'language', 'owner', 'registered_date', 'modified_date', 'status')

    list_filter = ('author', 'publisher', 'language', 'status')

    radio_fields = {'status': admin.VERTICAL}

class ShelfAdmin(ModelAdmin):
    fieldsets = (
        (
            'Position', {
                'fields': (('row', 'col'),)
            }
        ),
        (
            'Assigned Book', {
                'fields': ('current_book',)
            }
        ),
        (None, {'fields': ('shelf_status',)})
    )

    list_display = ('row', 'col', 'current_book', 'shelf_status')

admin.site.register(Book, BookAdmin)
admin.site.register(Shelf, ShelfAdmin)