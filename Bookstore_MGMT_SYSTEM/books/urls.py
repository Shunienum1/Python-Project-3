# books/urls.py
from django.urls import path
from . import views
from .views import index, book_create, search_books, post_login, book_detail, book_list, book_edit, book_delete
from django.contrib.auth.views import LogoutView

app_name = 'books'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.book_create, name='book_add'),
    path('search/', views.search_books, name='book_search'),
    path('post-login/', views.post_login, name='post_login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/', views.book_list, name='book_list'),
    path('book/edit/<int:book_id>/', book_edit, name='book_edit'),
    path('book/delete/<int:book_id>/', book_delete, name='book_delete'),
    path('inventory-summary/', views.inventory_summary, name='inventory_summary'),
    path('shelf-detail/<str:shelf>/', views.shelf_detail, name='shelf_detail'),
]
