from django import forms
from .models import ContactUs, Newsletter

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'company_name', 'email', 'subject', 'message']


class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'})
    )

    class Meta:
        model = Newsletter
        fields = ['email']
