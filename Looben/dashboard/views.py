from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse

from accounts.models import Users
from reviews.models import ReviewOfUniversity

from .forms import PostForm
from .models import Post


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
        context['form'] = PostForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostForm(request.POST or None)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard:post_in_dashboard', username=request.user.username)
        else:
            context = self.get_context_data()
            context['form'] = form  # form.is_validしたフォームを渡さないと、フォームのエラーを表示できない
            return render(request, 'dashboard/post_in_dashboard.html', context)    
    
    
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
