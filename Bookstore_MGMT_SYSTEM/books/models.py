from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=255)
    original_language = models.CharField(max_length=50)
    first_published = models.IntegerField()
    sales_millions = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=100)
    shelves = models.CharField(max_length=50)
    number_of_books = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
