from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .models import Book
from django.forms import ModelForm
from .forms import BookSearchForm

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
            return redirect('books:book_add')  # Redirect back to the book creation page
    else:
        form = BookForm()

    return render(request, 'books/book_form.html', {'form': form})

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'original_language', 'first_published', 'sales_millions', 'genre', 'shelves', 'number_of_books', 'price']

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
        messages.success(request, "The book was deleted successfully!")
        return redirect('books:book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        # Redirect to the book list after deletion
        return redirect('books:book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})