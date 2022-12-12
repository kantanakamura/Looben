from django import forms

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
    url = forms.CharField(label='URL', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'URL記入欄', 
        'id': 'url',
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
        fields = ['title', 'meta_description', 'url', 'top_image', 'tag']
        
        
class EditBlogPostForm(forms.ModelForm):
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
    url = forms.CharField(label='URL', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'URL記入欄', 
        'id': 'url',
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
        fields = ['title', 'meta_description', 'url', 'top_image', 'tag']