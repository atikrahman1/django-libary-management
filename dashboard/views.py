from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from dashboard.models import books
from django.contrib.sessions.models import Session


# Create your views here.

def home_screen_view(request):
    context = {}
    book_list = books.objects.all()

    book = Paginator(book_list,8)

    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1

    book_list = book.get_page(page)

    context = {
        'books': book_list,
    }

    if request.user.is_authenticated:
        username = request.session['username']
        user = User.objects.get(username=username)
        count = user.books_set.all()
        context["count"] = count

    return render(request, "dashboard/home.html", context)


def search(request):

    if request.GET.get('q'):
        query = request.GET.get('q')
        querySet = []
        context = {}
        queries = str(query).split(" ")

        for idx,q in enumerate(queries):
            booksresult = books.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(author__icontains=q)
            ).distinct()

            for result in booksresult:
                querySet.append(result)

    final_result = list(set(querySet))

    context = {
        'results': final_result,
        'query'  : query,
    }

    return render(request, "dashboard/home.html",context)
