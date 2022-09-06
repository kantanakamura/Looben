from multiprocessing import connection
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.http import HttpResponseRedirect

from .models import ReviewOfUniverity
from .forms import ReviewForm

from accounts.models import Users


class CreateReviewOfUniversityView(CreateView):
    template_name = 'reviews/create_review_of_university.html'
    form_class = ReviewForm
    success_message = 'レビューを作成しました'
    
    # def get_success_url(self):
    #     return reverse_lazy('reviews:user_login')  
    
    
