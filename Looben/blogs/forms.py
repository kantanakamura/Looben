from dataclasses import field
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import PasswordChangeForm

from .models import Blog

class CreateBlogForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'タイトル記入欄', 
        'id': '',
        }))
    content = forms.CharField(label='記事内容', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '記事記入欄',
        'rows': '10',
        'type': 'textarea',
        }))
    top_image = forms.FileField(label='サムネイル画像', widget=forms.FileInput(attrs={
        'class': 'form-control', 
        'type': 'file',
        'id': 'formFile',
        }))
    
    class Meta:
        model = Blog
        fields = ['title', 'content']
        