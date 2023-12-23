from django import forms
from django.db import models
from django.forms import fields, Widget
from .models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='Category Name', widget=forms.TextInput(attrs={'class': 'span6 typeahead', 'placeholder':'Category Name'}), required=True, error_messages={'required':'Must Enter a Correct Name'})
    class Meta:
        model = Category
        fields = ['id', 'name']
        widgets = {
            
        }