from django.urls import path
from . import views 

urlpatterns = [
    path('list/', views.book_listview, name='book_list'),
    path('author/', views.author_listview, name='author_listview'),
    path('books/create/', views.add_book, name='add_book'),
    path('books/update/<int:book_id>/', views.update_book, name='update_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]