# urls.py (project-level)
from django.contrib import admin
from django.urls import path, include
from books.views import SignUpView
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Includes login, logout, and password management URLs
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', views.index, name='index'),
    path('', include('books.urls', namespace='books')),  # Including the 'books' app URLs with namespace
]
