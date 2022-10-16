from dataclasses import field
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import PasswordChangeForm

from .models import Majors, Schools, Users


#　アカウント作成フォーム
class RegistForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーネーム', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter username', 
        'id': 'specificSizeInputGroupUsername',
        }))
    email = forms.EmailField(label='メールアドレス', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter email', 
        'id': '',
        'type': 'email'
        }))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={
        'class': 'form-control fakepassword', 
        'placeholder': 'Enter password',
        'id': 'psw-input',
        'type': 'password'
        }))
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter password again',
        'id': '',
        'type': 'password'
        }))
    
    class Meta:
        model = Users
        fields = ['username', 'email', 'password']
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')
    
    
#　ユーザーログインフォーム
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'name@example.com', 
        'id': 'floatingInput'
        }))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Password',
        'id': 'floatingPassword',
        }))
        
        
# ユーザー詳細設定のフォーム
class AccountSettingForm(forms.ModelForm):
    picture = forms.FileField(label='プロフィール画像', widget=forms.FileInput(attrs={
        'class': 'form-control', 
        'type': 'file',
        'id': 'formFile',
        }))
    name = forms.CharField(label='名前', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'ノエーボ太郎 (必須)', 
        'type': 'text'
        }))
    username = forms.CharField(label='ユーザーネーム', widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'looben_taiwan (必須)', 
        'type': 'text',
        'id': 'specificSizeInputGroupUsername',
        }))
    birthday = forms.DateField(label='生年月日', widget=forms.SelectDateWidget(years=[x for x in range(1923, 2023)], attrs={
        'class': 'form-control', 
        'placeholder': '2001-05-04 (必須)',
        'type': 'select',
        }))
    individual_theme_color = forms.CharField(label='テーマカラー', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'type': 'color',
        }))
    instagram_account_name = forms.CharField(label='Instagram', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'looben_taiwan (任意)',
        'type': 'text',
        }))
    twitter_account_name = forms.CharField(label='Twitter', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'looben_taiwan (任意)',
        'type': 'text',
        }))
    description = forms.CharField(label='profile', widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': '自己紹介 (必須)',
        'rows': '5',
        'type': 'textarea',
        }), max_length=160)
    major = forms.ModelChoiceField(label='学科', required=False, queryset= Majors.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': '〇〇学部・学科 (任意)',
        'type': 'select',
        }))
    school = forms.ModelChoiceField(label='大学', required=False, queryset= Schools.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': '大学 (任意)',
        'type': 'select',
        }))
    state = forms.ChoiceField(label='所属', choices=(('現役台湾留学生', '現役台湾留学生'), ('台湾留学卒業生','台湾留学卒業生'), ('留学興味あり','留学興味あり'),('その他','その他')), widget=forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': '所属',
        'type': 'select',
        }))
    
    
    class Meta:
        model = Users
        fields = ['picture', 'name', 'username', 'birthday', 'instagram_account_name', 'twitter_account_name', 'description', 'major', 'school', 'state', 'individual_theme_color']
        
    def save(self, *args, **kwargs):
        obj = super(AccountSettingForm, self).save(commit=False)
        obj.save()
        return obj
            

#　パスワード変更フォーム
class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Password',
        'id': 'floatingPassword',
        }))
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Password again',
        'id': 'floatingPassword',
        }))
    
    class Meta:
        model = Users
        fields = ['password',]
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user