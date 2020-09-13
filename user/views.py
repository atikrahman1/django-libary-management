from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import *

# Create your views here.

@login_required(login_url='login')
def user_profile(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    books_user = user.books_set.all()

    args = {
            'user': request.user,
            'books_user': books_user,
           }

    return render(request, "user/profile.html", args)

@login_required(login_url='login')
def book_operation(request):

    action = request.GET.get('action')
    b_id = request.GET.get('b_id')
    username = request.session['username']
    user = User.objects.get(username=username)
    book = get_object_or_404(books,id=b_id)

    if request.method == 'GET' and ('action' or 'b_id') not in request.GET:
        return HttpResponse('action or b_id is not present!')
    elif action == 'add':
        add = book.user_id.add(user)
        return HttpResponse(book.name + ' Added sucessfully')
    elif action == 'remove':
        remove = book.user_id.remove(user)
        return HttpResponse(book.name + ' deleted sucessfully')
    else:
        return HttpResponse('Unknown action defined!!')