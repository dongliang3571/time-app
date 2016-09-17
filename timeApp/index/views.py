from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import SignInForm
from session.models import TemporalUser, UserSession


def index(request):
    if request.user.is_authenticated():
        return redirect('session-members')
    else:
        context = {}
        form = SignInForm()
        context['form'] = form
        return render(request, 'index/index_index.html', context)

def about(request):
    template_name = "index/index_about.html"
    return render(request, template_name)

def faq(request):
    template_name = "index/index_faq.html"
    return render(request, template_name)
