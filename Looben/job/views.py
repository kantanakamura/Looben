from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404  
from django.http import JsonResponse

from .forms import CreateJobExperienceForm, UpdateJobExperienceForm
from .models import JobExperience
from chat.models import ConversationPartner
from notifications.models import Notification


@login_required
def create_job_experience(request):
    create_job_experience_form = CreateJobExperienceForm(request.POST or None, files=request.FILES)
    if create_job_experience_form.is_valid():
        create_job_experience_form.instance.user = request.user
        create_job_experience_form.save()
        return redirect('dashboard:post_in_dashboard', username=request.user.username)
    notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
    number_of_notification =  Notification.objects.filter(receiver=request.user).count()
    has_notifications =  Notification.objects.filter(receiver=request.user).exists()
    has_not_seen_message = ConversationPartner.objects.filter(current_user=request.ser, have_new_message=True).exists()
    return render(request, 'job/create_job_experience.html', context={
        'create_job_experience_form': create_job_experience_form,
        'notification_lists': notification_lists,
        'number_of_notification': number_of_notification,
        'has_notifications': has_notifications,
        'has_not_seen_message': has_not_seen_message
    })
    
    
class CheckForUserMatchMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        target_job_experience = get_object_or_404(JobExperience, pk=self.kwargs['pk'])
        return self.request.user == target_job_experience.user
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Only user who made this author have access to this view'}
        )
    

class UpdateJobExperienceView(CheckForUserMatchMixin, UpdateView):
    template_name = 'job/update_job_experience.html'
    form_class = UpdateJobExperienceForm
    model = JobExperience
    
    def get_success_url(self):
        return reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': self.object.user.username})
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context
        

class DeleteJobExperienceView(CheckForUserMatchMixin, DeleteView):
    template_name = 'job/delete_job_experience.html'
    model = JobExperience
    
    def get_success_url(self):
        return reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': self.object.user.username})
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context