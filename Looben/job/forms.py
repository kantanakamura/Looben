from dataclasses import field
from django import forms

from .models import JobExperience


class CreateJobExperienceForm(forms.ModelForm):
    company_name = forms.CharField(label='企業名', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': '活動タイトル記入欄', 
        }))
    job_date = forms.DateField(label='期間', widget=forms.SelectDateWidget(years=[x for x in range(2000, 2023)], attrs={
        'class': 'form-control', 
        'type': 'select',
        }))
    job_content = forms.CharField(label='仕事内容', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': '活動内容記入欄', 
        }))
    job_picture = forms.FileField(label='アイコン画像', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 
        'type': 'file',
        'id': 'formFile',
        }))
    
    class Meta:
        model = JobExperience
        fields = ['company_name', 'job_date', 'job_content', 'job_picture']
        
        
class UpdateJobExperienceForm(forms.ModelForm):
    company_name = forms.CharField(label='企業名', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': '活動タイトル記入欄', 
        }))
    job_date = forms.DateField(label='期間', widget=forms.SelectDateWidget(years=[x for x in range(2010, 2024)], attrs={
        'class': 'form-control', 
        'type': 'select',
        }))
    job_content = forms.CharField(label='仕事内容', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': '活動内容記入欄', 
        }))
    job_picture = forms.FileField(label='アイコン画像', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 
        'type': 'file',
        'id': 'formFile',
        }))
    
    class Meta:
        model = JobExperience
        fields = ['company_name', 'job_date', 'job_content', 'job_picture']