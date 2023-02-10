from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .models import Notification
from chat.models import ConversationPartner
        
        
class NotificationList(LoginRequiredMixin, TemplateView): 
    template_name = 'notifications/notification_list.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['all_notification_list'] = Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse().all()
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context

    
def delete_all_notifications(request):
    Notification.objects.filter(receiver=request.user).delete()
    return render(request, 'notifications/notification_list.html')

