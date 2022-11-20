from dataclasses import field
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import PasswordChangeForm
from mdeditor.fields import MDTextFormField

from .models import Blog

class CreateBlogForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'タイトル記入欄', 
        'id': 'title',
        }))
    meta_description = forms.CharField(label='メタデスクリプション', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'rows': '5',
        'type': 'textarea',
        'id': 'meta_description',
        }))
    content = MDTextFormField(label='記事内容', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '記事記入欄',
        'rows': '10',
        'type': 'textarea',
        'id': 'content',
        }))
    top_image = forms.FileField(label='サムネイル画像', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 
        'type': 'file',
        'id': 'formFile',
        }))
    tag = forms.CharField(label='タグ', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'id': 'tag',
        }))
    
    
    class Meta:
        model = Blog
        fields = ['title', 'meta_description', 'content', 'top_image', 'tag']
        
        
class EditBlogPostForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'タイトル記入欄', 
        'id': '',
        }))
    meta_description = forms.CharField(label='メタデスクリプション', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '',
        'rows': '5',
        'type': 'textarea',
        }))
    content = MDTextFormField(label='記事内容', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '記事記入欄',
        'rows': '10',
        'type': 'textarea',
        }))
    top_image = forms.FileField(label='サムネイル画像', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 
        'type': 'file',
        'id': 'formFile',
        }))
    tag = forms.CharField(label='タグ', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': '', 
        'id': '',
        }))
    
    
    class Meta:
        model = Blog
        fields = ['title', 'meta_description', 'content', 'top_image', 'tag']