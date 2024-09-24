
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from .models import Book
from .models import Author
from django.contrib import messages
# Create your views here.


def book_listview(request):
    books = Book.objects.all()  # Get all books
    context = {
        'books': books
    }
    return render(request, 'book/book_list.html', context)


def author_listview(request):
    author = Author.objects.all()  # Get all author
    context = {
        'author': author
    }
    return render(request, 'book/author.html', context)


def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        isbn = request.POST.get('isbn')
        published_date = request.POST.get('published_date')
        available_copies = request.POST.get('available_copies')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Handle author creation or fetching existing author
        author, created = Author.objects.get_or_create(name=author_name)

        # Create and save the book instance
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            published_date=published_date,
            available_copies=available_copies,
            description=description,
            image=image,
            entry_by=request.user  
        )
        book.save()
        messages.success(request, 'Book Add successfully.')

        return redirect('book_list')  
    else:
        
        messages.error(request, 'Please fill in all required fields.')

    return render(request, 'book/create_book.html')  


#update Book
def update_book(request, book_id):
    # Get the book instance by ID or return a 404 error if not found
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_name = request.POST.get('author')
        book.isbn = request.POST.get('isbn')
        book.published_date = request.POST.get('published_date')
        book.available_copies = request.POST.get('available_copies')
        book.description = request.POST.get('description')
        
        # Handle author creation or fetching existing author
        author, created = Author.objects.get_or_create(name=author_name)
        book.author = author
        
        # Check for an image upload
        if request.FILES.get('image'):
            book.image = request.FILES.get('image')

        # Save the updated book instance
        book.save()
        messages.success(request, 'Book updated successfully.')

        return redirect('book_list')

    context = {
        'book': book
    }
    return render(request, 'book/update_book.html', context)



def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('book_list') 

    