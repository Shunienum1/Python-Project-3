from django.core.management.base import BaseCommand, CommandError
import csv
from books.models import Book  # Adjust this import to your model's path

class Command(BaseCommand):
    help = 'Imports books from a specified CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The CSV file path')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Create a Book instance for each row in the CSV
                Book.objects.create(
                    title=row['Book'],
                    authors=row['Author(s)'],
                    original_language=row['Original language'],
                    first_published=row['First published'],
                    sales_millions=row['Approximate sales in millions'],
                    genre=row.get('Genre', ''),  # Assuming it can be optional
                    shelves=row['Shelves'],
                    number_of_books=row['Number of Books'],
                    price=row['Price'],
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported book data.'))
