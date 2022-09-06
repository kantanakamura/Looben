from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView

from accounts.models import Users

class PostInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/post_in_dashboard.html'
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number_of_friends = self.object.connection.all().count()
        # ユーザーの友達の数
        context['number_of_friends'] = number_of_friends
        return context
    
    
class ReviewInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/review_in_dashboard.html'
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'