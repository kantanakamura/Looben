from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse

from accounts.models import Users
from blogs.models import Blog
from reviews.models import ReviewOfUniversity


class PostInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/post_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = user.connection.all().count()
        context['number_of_followed_user'] = user.connected_users.all().count()
        context['saved_user_sidebar_list'] = user.saved_users.all()[:4]
        context['blog_posts'] = Blog.objects.filter(author=user).all()
        return context
    
    
class ReviewInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/review_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = user.connection.all().count()
        context['number_of_followed_user'] = user.connected_users.all().count()
        context['saved_user_sidebar_list'] = user.saved_users.all()[:4]
        context['reviews'] = ReviewOfUniversity.objects.filter(user=user).all()
        return context
    

class FollowingInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/following_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = user.connection.all().count()
        context['number_of_followed_user'] = user.connected_users.all().count()
        context['saved_user_sidebar_list'] = user.saved_users.all()[:4]
        return context
    
    
class FollowedInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/followed_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = user.connection.all().count()
        context['number_of_followed_user'] = user.connected_users.all().count()
        context['saved_user_sidebar_list'] = user.saved_users.all()[:4]
        return context

    
class QuestionInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/question_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = user.connection.all().count()
        context['number_of_followed_user'] = user.connected_users.all().count()
        context['saved_user_sidebar_list'] = user.saved_users.all()[:4]
        context['asked_questions'] = user.questions_set.filter(is_anonymous=False).all()
        return context
