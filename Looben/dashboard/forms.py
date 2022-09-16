from dataclasses import field
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(label='投稿', widget=forms.Textarea(attrs={
        'class': 'form-control pe-4 fs-3 lh-1 border-0', 
        'placeholder': 'Share your thoughts...',
        'rows': '5',
        'type': 'textarea',
        # 'autofocus': '',
        }))

    
    class Meta:
        model = Post
        fields = ['content'] 