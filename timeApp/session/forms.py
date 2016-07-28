from django.core.urlresolvers import reverse
from django import forms

from .models import Team, TemporalUser


class TemporalUserCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'})
        )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'})
        )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'})
        )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
            })
        )

    class Meta:
        model = TemporalUser
        fields = ['first_name', 'last_name', 'email', 'team']


class DateFilterForm(forms.Form):
    start_date = forms.CharField(
        label='Start date',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': '01/05/2016'})
        )
    end_date = forms.CharField(
        label='End date',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': '02/05/2016'})
        )
    keyword = forms.CharField(
        label='Keyword Search',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type in Team name...'})
        )
