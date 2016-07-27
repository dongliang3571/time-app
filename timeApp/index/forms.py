from django import forms
from django.contrib.auth.models import User


class SignInForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control'
            })
        )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
            })
        )
