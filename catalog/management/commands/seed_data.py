from typing import NoReturn

from django.core.management.base import BaseCommand
from faker import Faker  # fake the db
from factory.django import DjangoModelFactory  # extends faker capabilities
from factory import Sequence  # needed for establishing filling out manner. Acc func
import random
from ...models import Author, Book, BookInstance, Language, Genre, User
import datetime
import uuid

# python manage.py seed --mode=refresh
"""create a faker instance"""
fake = Faker()

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")
        parser.add_argument('-na', type=str, help="Number of seed authors")
        parser.add_argument('-ng', type=str, help="Number of seed genres")
        parser.add_argument('-nl', type=str, help="Number of seed languages")
        parser.add_argument('-nb', type=str, help="Number of seed books")
        parser.add_argument('-nbi', type=str, help="Number of seed book instances")

    def handle(self, *args, **options):
        numbers = [
            options['na'],
            options['ng'],
            options['nl'],
            options['nb'],
            options['nbi']
        ]

        # validate the numbers as valid integers
        for index, input_item in enumerate(numbers):
            num = self.to_int(input_item)
            if num == -1:
                print(
                    'You inserted an invalid number so the default is set as 0 (nothing will be seeded)'
                )
                break
            numbers[index] = num

        else:
            self.stdout.write('seeding data...')
            authors_num, genres_num, languages_num, books_num, book_inst_num = tuple(numbers)
            self.run_seed(
                options['mode'],
                authors_serve=(self.create_author, authors_num),
                genres_serve=(self.create_genre, genres_num),
                languages_serve=(self.create_language, languages_num),
                books_serve=(self.create_book, books_num),
                book_inst_serve=(self.create_book_instance, book_inst_num)
                )
            self.stdout.write('done.')

    @staticmethod
    def clear_data():
        """Deletes all the table data"""
        print("Delete All DB")
        Author.objects.all().delete()
        Genre.objects.all().delete()
        Language.objects.all().delete()
        BookInstance.objects.all().delete()
        Book.objects.all().delete()

    @staticmethod
    def create_language():
        """Creates genre object using Faker instance and langcodes to look real in the stdout"""
        print("Creating a fake language")
        language = Language(
            name=fake.language_name()
        )
        language.save()
        print("The {} language created.".format(language.name))
        return language

    @staticmethod
    def create_genre():
        """Creates genre object using Faker instance"""
        print("Creating a fake genre of who knows what letters")
        genre = Genre(
            name=''.join(
                fake.random_letters(
                    length=random.randint(4, 10)
                )
            )
            .title()
        )
        genre.save()
        print("The {} genre created.".format(genre.name))
        return genre

    @staticmethod
    def create_author():
        """create a fake author"""
        print("Creating a fake author")
        # faking birthdate and furthermore death date based on the date of birth
        fake_birth = datetime.datetime.strptime(fake.date(), '%Y-%m-%d')
        fake_death = fake_birth + datetime.timedelta(
            weeks=52 * random.randint(
                20, 80
            )
        )

        author = Author(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake_birth.strftime('%Y-%m-%d'),
            date_of_death=fake_death.strftime('%Y-%m-%d'),
            biography=fake.text()
        )

        author.save()
        print("The author {} {}, born {}, died {}, bio {} created.".format(
            author.first_name,
            author.last_name,
            author.date_of_birth,
            author.date_of_death,
            author.biography
        ))
        return author

    @staticmethod
    def create_book():
        """create a book using all the models above"""
        author = random.choice(Author.objects.all())
        genre = random.choice(Genre.objects.all())
        language = random.choice(Language.objects.all())
        book = Book(
            author=author,
            title=''.join(
                fake.random_letters(
                    length=random.randint(4, 10)
                )
            )
            .title(),
            summary=fake.text(),
            isbn=fake.isbn13().replace('-', ''),
            language=language

        )
        book.save()
        book.genre.add(genre)
        book.save()
        print("The book {} written by {} created.".format(
            book.title,
            f'{book.author.first_name} {book.author.last_name}'
        ))

        return book
        # TODO can be int

    @staticmethod
    def create_book_instance():
        """create a book using all the models above"""
        book_inst = BookInstance(
            id=uuid.uuid4(),
            book=random.choice(Book.objects.all()),
            imprint=fake.text(),
            status=random.choice(
                (
                    'm',
                    'o',
                    'a',
                    'r',
                )
            )
        )
        book_inst.save()
        # borrower and due back depends on whether the book is on loan or not
        if book_inst.status == 'o':
            book_inst.due_back = (datetime.datetime.now() + datetime.timedelta(
                days=random.randint(7, 31)
            )).strftime("%Y-%m-%d")
            book_inst.borrower = random.choice(User.objects.all())
            book_inst.save()

        print("The book instance {} written by {} created.".format(
            book_inst.book.title,
            f'{book_inst.book.author.first_name} {book_inst.book.author.last_name}'
        ))

    def run_seed(self, mode: str, **kwargs):
        """ Seed database based on mode
        :self: the class inst
        :param mode: refresh / clear
        :return:
        """
        # Clear data from tables
        self.clear_data()
        if mode == MODE_CLEAR:
            return

        # Creating the set number of objects to create
        for i_struct in kwargs.values():
            func, value = i_struct
            for _ in range(value):
                func()

    @staticmethod
    def to_int(item: str) -> int or NoReturn:
        """
        method takes the item and checks if it is a valid integer.
        Limited to 1000 seeds
        """
        try:
            item = int(item)
        except ValueError:
            raise NotImplementedError('The {item} is not an int! Cannot prepare for seed!'.format(
                item=item
            ))
        else:
            return item if 0 < item <= 1000 else -1
