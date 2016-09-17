from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .models import ContactUs, Newsletter
from .forms import ContactUsForm, NewsletterForm


def index(request):
    if request.user.is_authenticated():
        return redirect('session-members')
    else:
        return render(request, 'index/index_index.html')

def about(request):
    template_name = "index/index_about.html"
    return render(request, template_name)

def faq(request):
    template_name = "index/index_faq.html"
    return render(request, template_name)

def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            subject = "Received a message from timeApp"
            message = ("Person name: " + instance.name + "\nEmail: " + instance.email +
                        "\nMessage: " + instance.message )
            from_email = settings.EMAIL_HOST_USER
            to_list = ['dongliang3571@gmail.com']
            flag = send_mail(subject, message, from_email, to_list, fail_silently=False)
            if flag == 1:
                messages.success(request, 'Thank you for sending the message!')
                return redirect(reverse('index-index'))
            else:
                messages.error(request, 'Failed to send messages!')
                return redirect(reverse('index-contact'))
        else:
            messages.error(request, 'Failed to send messages!')
            return redirect(reverse('index-contact'))
    else:
        template_name = 'index/index_contact.html'
        return render(request, template_name)

def newsletter(request):
    form = NewsletterForm(request.POST or None)
    form.required_css_class = 'newsletter_email'
    if form.is_valid():
        form.save()
        subject = "Someone subscribed KlokIn"
        message = "email is: " + form.cleaned_data['email']
        from_email = settings.EMAIL_HOST_USER
        to_list = ['dongliang3571@gmail.com']
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        messages.success(request, 'Thank you for subscribing')
        return redirect(reverse('index-index'))
    else:
        messages.error(request, 'Invalid email')
        return redirect(reverse('index-newsletter-id'))
