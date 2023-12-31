from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from django.contrib.auth.models import User  # import a user instance to test
# against book borrowing facilitation feature
from datetime import date


# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        help_text='Enter a book genre (e.g. Science Fiction)'
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Language(models.Model):
    """Model representing a language of a book in our library."""
    name = models.CharField(
        verbose_name='Language',
        max_length=100,
        help_text='Enter a book language (e.g. English)'
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(verbose_name='Born', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    biography = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (
            ('can_affect_authors', 'Can affect authors'),
        )

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def get_url_to_edition(self):
        """returns the URL to edit page."""
        return reverse('author-update', args=[str(self.id)])

    def get_url_to_deletion(self):
        """returns the URL to delete page."""
        return reverse('author-delete', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author is a string rather than an object because it hasn't been declared yet in the file
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000,
        help_text='Enter a brief description of the book'
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='13-digit code')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined, so we can specify the object above.
    genre = models.ManyToManyField(
        Genre,
        help_text='Select a genre for this book'
    )

    # add ordering field
    ordering = ['title']

    # add language attr
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse(
            'book-detail',
            args=[str(self.id)]
        )

    def get_url_to_edition(self):
        """returns the URL to edit page."""
        return reverse(
            'book-update',
            args=[str(self.id)]
        )

    def get_url_to_deletion(self):
        """returns the URL to delete page."""
        return reverse(
            'book-delete',
            args=[str(self.id)]
        )

    class Meta:
        permissions = (
            ('can_affect_books', 'Can affect books'),
            ('can_mark_returned', 'Set book as returned'),
        )

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(
        'Book',
        on_delete=models.RESTRICT,
        null=True
    )
    imprint = models.CharField(
        max_length=200
    )
    due_back = models.DateField(
        null=True,
        blank=True
    )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['due_back']
        permissions = (
            ("view_all_borrowed", "View all borrowed books"),
            ("can_mark_returned", "Can mark returned"),
        )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

    def is_overdue(self) -> bool:
        """This method returns a boolean indicating whether the model is borrowed and overdue"""
        return bool(self.due_back and date.today() > self.due_back)
