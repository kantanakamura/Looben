from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.urls import reverse

from accounts.models import Users
from reviews.models import ReviewOfUniversity
from .forms import PostForm
from .models import Post

class PostInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/post_in_dashboard.html'
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'
    
    def get_success_url(self):
        return reverse('dashboard:post_in_dashboard', kwargs={'username': self.object.username })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォローしている人の数
        number_of_following_user = self.object.connection.all().count()
        context['number_of_following_user'] = number_of_following_user
        # フォローされている人の数
        number_of_followed_user = self.object.connected_users.all().count()
        context['number_of_followed_user'] = number_of_followed_user
        saved_user_sidebar_list = self.object.saved_users.all()[:4]
        context['saved_user_sidebar_list'] = saved_user_sidebar_list
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            create_post_form = PostForm(request.POST or None)
            create_post_form.instance.user = request.user
            create_post_form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(Post, self).form_valid(form)
    
    
class ReviewInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/review_in_dashboard.html'
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォローしている人の数
        number_of_following_user = self.object.connection.all().count()
        context['number_of_following_user'] = number_of_following_user
        # フォローされている人の数
        number_of_followed_user = self.object.connected_users.all().count()
        context['number_of_followed_user'] = number_of_followed_user
        saved_user_sidebar_list = self.object.saved_users.all()[:4]
        context['saved_user_sidebar_list'] = saved_user_sidebar_list
        user = self.object
        context['reviews'] = ReviewOfUniversity.objects.filter(user=user).all()
        return context
    

class FollowingInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/following_in_dashboard.html'
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォローしている人の数
        number_of_following_user = self.object.connection.all().count()
        context['number_of_following_user'] = number_of_following_user
        # フォローされている人の数
        number_of_followed_user = self.object.connected_users.all().count()
        context['number_of_followed_user'] = number_of_followed_user
        saved_user_sidebar_list = self.object.saved_users.all()[:4]
        context['saved_user_sidebar_list'] = saved_user_sidebar_list
        return context
    
    
class FollowedInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/followed_in_dashboard.html'
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォローしている人の数
        number_of_following_user = self.object.connection.all().count()
        context['number_of_following_user'] = number_of_following_user
        # フォローされている人の数
        number_of_followed_user = self.object.connected_users.all().count()
        context['number_of_followed_user'] = number_of_followed_user
        saved_user_sidebar_list = self.object.saved_users.all()[:4]
        context['saved_user_sidebar_list'] = saved_user_sidebar_list
        return context

    
