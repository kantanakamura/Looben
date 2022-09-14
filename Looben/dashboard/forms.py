from dataclasses import field
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(label='投稿', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': '投稿',
        'type': 'text',
        }))

    
    class Meta:
        model = Post
        fields = ['content'] 