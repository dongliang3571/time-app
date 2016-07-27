from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import SignInForm
from session.models import TemporalUser, UserSession


def index(request):
    context = {}
    form = SignInForm()
    context['form'] = form
    return render(request, 'dashboard/index.html', context)


def organizationLogin(request):
    context = {}
    print "here"
    if request.method == 'POST':
        form = SignInForm(request.POST)
        context['form'] = form
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard-dashboard')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, "dashboard/index.html", context)
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'dashboard/index.html', context)
    else:
        form = SignInForm()
        context['form'] = form
        return render(request, 'dashboard/index.html', context)


def organizationLogout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('index-index')


def dashboard(request):
    messages.error(request, 'haha')
    return render(request, 'dashboar/dashboard.html')
