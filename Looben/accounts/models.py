from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from email.policy import default
from tabnanny import verbose
from tkinter import CASCADE


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('メールアドレスを必ず入力してください')
        elif not username:
            raise ValueError('ユーザーネームを入力してください')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    
class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    connection = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='connected_users')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    individual_theme_color = models.CharField(max_length=10, default='#D5E9FF')
    picture = models.FileField(blank=True, upload_to='pfp/', default='pfp/unknown_user.png')
    name = models.CharField(max_length=130, blank=True)
    birthday = models.DateField(null=True)
    instagram_account_name = models.CharField(max_length=150, blank=True)
    twitter_account_name = models.CharField(max_length=150, blank=True)
    description = models.TextField(max_length=150, blank=True)
    saved_users = models.ManyToManyField('self', symmetrical=False, blank=True)
    saved_university = models.ManyToManyField('Schools', symmetrical=False, blank=True, related_name='saved_university_users')
    state = models.CharField(max_length=50, default='その他')
    joined_at = models.DateField(default=timezone.now)
    contributed_points = models.IntegerField(default=0)
    major = models.ForeignKey(
        'Majors', on_delete=models.CASCADE, null=True
    )
    school = models.ForeignKey(
        'Schools', on_delete=models.CASCADE, null=True, related_name='school_users'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def get_absolute_url(self):
        return reverse_lazy('accounts:home')
    
    class Meta:
        verbose_name_plural = 'ユーザー'
        
    def __str__(self):
        return self.username + ' : ' + str(self.school)
        


class Schools(models.Model):
    name = models.CharField(max_length=150)
    major = models.ManyToManyField('Majors')
    is_national = models.BooleanField(default=False)
    place = models.CharField(max_length=150, null=True)
    picture = models.FileField(blank=True, upload_to='university/')
    address = models.CharField(max_length=150, null=True)
    homepage = models.CharField(max_length=150, null=True)
    average_academic_fee = models.CharField(max_length=50, null=True)
    average_domitary_fee = models.CharField(max_length=50, null=True)
    number_of_students = models.IntegerField(null=True)
    description = models.CharField(max_length=260, null=True)
    youtube_url = models.CharField(max_length=200, null=True)
    sub_title = models.CharField(max_length=100, default='自然豊かな、経済学に強い大学')
    googlemap_url = models.CharField(max_length=300, default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.9663095343008!2d-74.00425878428698!3d40.74076684379132!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259bf5c1654f3%3A0xc80f9cfce5383d5d!2sGoogle!5e0!3m2!1sen!2sin!4v1586000412513!5m2!1sen!2sin')
    number_of_viewer = models.IntegerField(default=0)
    star_rating = models.IntegerField(default=3)
    
    class Meta:
        db_table = 'schools'
        verbose_name_plural = '大学'
        
    def __str__(self):
        return self.name
        


class Majors(models.Model):
    name = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'majors'
        verbose_name_plural = '学部学科'
        
    def __str__(self):
        return self.name
    
    