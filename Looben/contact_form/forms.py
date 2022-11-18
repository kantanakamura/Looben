from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse


class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    # Problem: [Errno 61] Connection refused　というエラーが起こるため改善が必要
    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        
        send_mail(
            name,
            message,
            email,
            ['looben2022@gmail.com'],
            fail_silently=False,
        )
        