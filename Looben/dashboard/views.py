from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse

from accounts.models import Users, FollowForUser
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
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['blog_posts'] = Blog.objects.filter(author=user).all()
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
    
    
class ReviewInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/review_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['reviews'] = ReviewOfUniversity.objects.filter(user=user).all()
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
    

class FollowingInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/following_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
    
    
class FollowedInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/followed_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context

    
class QuestionInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/question_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['asked_questions'] = user.questions_set.filter(is_anonymous=False).all()
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
