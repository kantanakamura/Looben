from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import CreateJobExperienceForm
from .models import JobExperience


@login_required
def create_job_experience(request):
    create_job_experience_form = CreateJobExperienceForm(request.POST or None, files=request.FILES)
    if create_job_experience_form.is_valid():
        create_job_experience_form.instance.user = request.user
        create_job_experience_form.save()
        return redirect('dashboard:post_in_dashboard', username=request.user.username)
    return render(request, 'job/create_job_experience.html', context={
        'create_job_experience_form': create_job_experience_form
    })