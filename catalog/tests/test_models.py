from django.test import TestCase
from django.db import models
from ..models import Author, Book, Language


class AuthorBooksModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')
        Book.objects.create(
            title='Some Book'
        )  # TODO lang?

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

    def test_if_models_can_get_url_to_edit_and_remove(self):
        author = Author.objects.get(id=1)
        book = Book.objects.get(id=1)
        # This will fail if any of the links to the edition or removal are broken
        # author models
        self.assertEqual(
            author.get_url_to_edition(), '/catalog/author/1/update/'
        )
        self.assertEqual(
            author.get_url_to_deletion(), '/catalog/author/1/delete/'
        )

        # same as above, but for book models
        self.assertEqual(
            book.get_url_to_edition(), '/catalog/book/1/update/'
        )
        self.assertEqual(
            book.get_url_to_deletion(), '/catalog/book/1/delete/'
        )

    def test_all_books_have_language(self):
        """if all books have a language field that is not empty"""
        book = Book.objects.all()  # TODO how to access all books here now?
        for i_book in book:
            continue
            print(i_book.language)
            self.assertIsNotNone(i_book.language)
