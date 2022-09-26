from dataclasses import field
from unicodedata import category
from django import forms

from .models import Questions, AnswerForQuestion
from accounts.models import Schools, Users


class QuestionForm(forms.ModelForm):
    content = forms.CharField(label='質問内容', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '質問内容',
        'type': 'textarea',
    }))
    university = forms.ModelChoiceField(label='質問する対象の大学', queryset= Schools.objects.all(), required=False, widget=forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': '質問する対象の大学',
        'type': 'select',
    }))
    category = forms.ChoiceField(label='カテゴリー', choices=(('university', '大学'), ('foods', '食事'), ('study', '勉強'), ('love', '恋愛'), ('life', '人生')), widget=forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'カテゴリー',
        'type': 'select',
    }))
    
    
    class Meta:
        model = Questions
        fields = ['content', 'university', 'category']
        
        
class AnswerForQuestionForm(forms.ModelForm):
    answer = forms.CharField(label='回答', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '回答記入欄',
        'type': 'textarea',
    }))
    
    class Meta:
        model = AnswerForQuestion
        fields = ['answer']