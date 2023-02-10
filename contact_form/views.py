from django.views.generic.base import TemplateView
from notifications.models import Notification
from chat.models import ConversationPartner


class ContactFormView(TemplateView):
    template_name = 'contact_form/contact_form.html'


class PrivacyAndSafetyView(TemplateView):
    template_name = 'contact_form/privacy_and_safety.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context