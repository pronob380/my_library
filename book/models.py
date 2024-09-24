from django.db import models

from user.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to='author_image/',
        blank=True,
        null=True 
    )

    def __str__(self):
        return self.name


    
class Book(models.Model):
    entry_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField()
    available_copies = models.IntegerField()
    image = models.ImageField(
        upload_to='book_image/',
        blank=True,
        null=True 
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

