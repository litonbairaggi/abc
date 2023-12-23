from django import forms
from django.db import models
from django.forms import fields, Widget
from .models import Myapp

class MyappForm(forms.ModelForm):
    name = forms.CharField(label='Myapp Name', widget=forms.TextInput(attrs={'class': 'span6 typeahead', 'placeholder':'Myapp Name'}), required=True, error_messages={'required':'Must Enter a Correct Name'})
    class Meta:
        model = Myapp
        fields = ['id', 'name']
        widgets = {
            
        }