from django.db import models
from django.conf import settings
from django.db.models.fields import BLANK_CHOICE_DASH
from simple_history.models import HistoricalRecords

# Create your models here.

class Book(models.Model):
    class Meta:
        unique_together = (('author', 'title'))
    IN_SHELF = 'AV'
    ON_HOLD = 'OH'
    MISSING = 'MS'
    IN_STORAGE = 'IS'
    STATUS = [
        (IN_SHELF, 'Available'),
        (ON_HOLD, 'On hold'),
        (MISSING, 'Missing'),
        (IN_STORAGE, 'In storage'),
    ]
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    picture = models.ImageField()
    status = models.CharField(max_length=255, choices=STATUS, default=ON_HOLD)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    history = HistoricalRecords()
    registered_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class Shelf(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['row', 'col'], name="It's a coordinate")
        ]
    ROW = [
        (1, 'Row 1'),
        (2, 'Row 2'),
        (3, 'Row 3'),
    ]
    COL = [
        (1, 'Column 1'),
        (2, 'Column 2'),
        (3, 'Column 3'),
    ]
    row = models.IntegerField(choices=ROW)
    col = models.IntegerField(choices=COL)
    current_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf_status = models.BooleanField(default=False)

