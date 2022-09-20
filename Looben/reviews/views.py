from multiprocessing import connection
from urllib import request
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

from .models import ReviewOfUniversity
from .forms import ReviewForm

from accounts.models import Users, Schools


    
def create_review_of_university(request):
    create_review_form = ReviewForm(request.POST or None)
    if create_review_form.is_valid():
        create_review_form.instance.user = request.user
        create_review_form.save()
        messages.success(request, 'レビューを作成しました')
        # Schoolsの星評価にこのレビューの評価を反映させる
        number_of_review = ReviewOfUniversity.objects.filter(university=create_review_form.cleaned_data.get('university')).count()
        target_university = Schools.objects.get(id=create_review_form.cleaned_data.get('university').id)
        target_university.star_rating = (target_university.star_rating + int(create_review_form.cleaned_data.get('star'))) / 2
        target_university.save()
        return redirect('accounts:research_university')
    return render(
        request, 'reviews/create_review_of_university.html', context={
            'create_review_form': create_review_form
        }
    )
    
    
class ReviewListOfUniversities(DetailView):
    model = Schools
    template_name = 'reviews/review_list_of_universities.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.object
        # この大学のレビューを取得
        context['reviews'] = ReviewOfUniversity.objects.filter(university=school)
        return context
    

