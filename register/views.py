from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib import messages


# Create your views here.

from .forms import CreateUserForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm (request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, "register/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            next = request.GET.get('next')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session['is_logged'] = True
                request.session['username'] = username
                if next:
                    return redirect(next)
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Username OR password is incorrect')
        return render(request, "register/login.html")

def logoutUser(request):
    logout(request)
    return redirect('login')
