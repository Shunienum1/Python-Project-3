from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .models import Book
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from .forms import BookSearchForm
from django.db.models import Count

# Function-based views
def index(request):
    return render(request, 'registration/index.html', {
        'message': "Welcome to our Bookstore!"
    })

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

# views.py
@login_required
def search_books(request):
    query = request.GET.get('query', '').strip()
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(authors__icontains=query)
    else:
        books = Book.objects.none()

    return render(request, 'books/book_search.html', {'books': books, 'query': query})


# Class-based views
class BookCreate(CreateView):
    model = Book
    fields = ['title', 'authors', 'original_language', 'first_published', 'sales_millions', 'genre', 'shelves', 'number_of_books', 'price']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        # Add custom success message or logic here if needed
        return super().form_valid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_staff = True
        user.is_superuser = True  # Make the user an admin
        user.save()
        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def post_login(request):
    # View that renders the page with options after login
    return render(request, 'registration/post_login.html')

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The book was added successfully!")
            return redirect('books:book_add')  # Or wherever you want to redirect after success
    else:
        form = BookForm()

    return render(request, 'books/book_form.html', {'form': form})


class BookForm(forms.ModelForm):
    SHELVES_CHOICES = [
        ('A', 'Shelf A'), ('B', 'Shelf B'), ('C', 'Shelf C'),
        ('D', 'Shelf D'), ('E', 'Shelf E'), ('F', 'Shelf F'),
        ('G', 'Shelf G'), ('H', 'Shelf H'),
    ]

    class Meta:
        model = Book
        fields = ['title', 'authors', 'original_language', 'first_published', 'sales_millions', 'genre', 'shelves', 'number_of_books', 'price']

    shelves = forms.ChoiceField(choices=SHELVES_CHOICES)

    def clean_first_published(self):
        first_published = self.cleaned_data['first_published']
        current_year = timezone.now().year
        if first_published > current_year:
            raise ValidationError('The first published year must be less than or equal to the current year.')
        return first_published

    def clean_sales_millions(self):
        sales_millions = self.cleaned_data['sales_millions']
        if sales_millions < 0:
            raise ValidationError('Sales in millions must be greater than or equal to 0.')
        return sales_millions

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Price must be greater than or equal to 0.')
        return price

    def clean_number_of_books(self):
        number_of_books = self.cleaned_data['number_of_books']
        if number_of_books < 0:
            raise ValidationError('Number of books must be greater than or equal to 0.')
        return number_of_books

    def clean_shelves(self):
        shelves = self.cleaned_data['shelves']
        valid_shelves = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if shelves not in valid_shelves:
            raise ValidationError('Shelves must be one of A, B, C, D, E, F, G, H.')
        return shelves

@login_required
def book_edit(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "The book was updated successfully!")
            return redirect('books:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})



@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        # Redirect to the book list after deletion
        return redirect('books:book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
def inventory_summary(request):
    shelves = Book.objects.values_list('shelves', flat=True).distinct()
    return render(request, 'books/inventory_summary.html', {'shelves': shelves})

from django.db.models import Sum

@login_required
def shelf_detail(request, shelf):
    # Query the database for books on the specific shelf
    # and aggregate the sum of the 'number_of_books' for each distinct book.
    books = Book.objects.filter(shelves=shelf)\
                .values('title', 'authors')\
                .annotate(total=sum('number_of_books'))\
                .order_by('title')
    # Get the count of distinct titles on the shelf
    distinct_books_count = books.count()
    return render(request, 'books/shelf_detail.html', {
        'books': books,
        'shelf': shelf,
        'distinct_books_count': distinct_books_count,
    })