from django.contrib import admin
from .models import Book, BookInstance, Language, Author, Genre


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # the order of demonstration attributes in the admin site
    list_display = (
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death'
    )

    fields = [
        'first_name',
        'last_name',
        ('date_of_birth', 'date_of_death'),
        'biography'
    ]
    inlines = [BookInline]  # TODO check this feature


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'display_genre',
        'language'
    )
    fieldsets = (
        ('General information', {
            'fields': ('title', 'author')
            }
         ),
        ('Description', {
            'fields': ('summary', 'isbn')
            }
         ),
        ('Category', {
            'fields': ('genre', 'language')
            }
         )
    )
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'status',
        'due_back',
        'id',
        'borrower'

    )
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


# Register your models here.
