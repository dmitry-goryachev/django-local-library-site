from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Book, Author, BookInstance, Genre
from django.views import generic
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class BookListView(generic.ListView):
    """View function for returning a list of all books"""
    model = Book
    ordering = ['title']
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """View function for returning a specific book detail"""
    model = Book


class AuthorListView(generic.ListView):
    """view function for returning a list of all authors"""
    model = Author
    paginate_by = 10
    ordering = ['last_name']

    # did it in frames of views expansion training
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rendered_time'] = datetime.datetime.now()
        return context


class AuthorDetailView(generic.DetailView):
    """view function for returning a specific author detail.
    produces rendering given the model below and passes variables"""
    model = Author


class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    """
    view allows the LOGGED-IN users from the group LIBRARIANS to view all the
    books borrowed in the library
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 10
    permission_required = "catalog.view_all_borrowed"

    def get_queryset(self):
        print(self.request.user.user_permissions.all())
        return (
            BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back')
        )


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    This view function displays all the books borrowed by the user
    if he is logged in
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


def index(request):
    """view function for home page of the site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = \
        BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.all().count()

    # add counts for books' genres
    num_genres = Genre.objects.all().count()

    # add counts for books with special filter:
    # The ones with name containing "and"
    num_books_with_and = Book.objects.filter(title__contains='and').count()

    # add number of visits to the main page counter
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # add info about is logged in
    is_logged_in = request.user.is_authenticated

    # context regarding thematic content
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_and': num_books_with_and,
        'num_visits': num_visits,  # add visit count
        'is_logged_in': is_logged_in,  # add is logged in status
    }

    # render the HTML template base_generic.html with the data in the context variable
    return render(
        request,
        'index.html',
        context
    )


@login_required()
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    """
    renew the book instance due back date. Requires special permissions.
    Need to be a librarian logged-in user
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    permission_required = "catalog.can_mark_returned"
    success_url = reverse_lazy('authors')


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'  # Not recommended (potential security issue if more fields added)
    permission_required = "catalog.can_affect_authors"


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = "catalog.can_affect_authors"


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = [
        'title',
        'author',
        'summary',
        'isbn',
        'genre',
        'language'
    ]
    initial = {'title': 'Some title', 'author': 'Some author'}
    permission_required = "catalog.can_affect_books"


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'  # Not recommended (potential security issue if more fields added)
    permission_required = "catalog.can_affect_books"


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = "catalog.can_affect_books"
