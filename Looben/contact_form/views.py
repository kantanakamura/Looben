from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactForm
from notifications.models import Notification
from chat.models import ConversationPartner


class ContactFormView(FormView):
    template_name = 'contact_form/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_form:contact_result')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context


class ContactResultView(TemplateView):
    template_name = 'contact_form/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context


class PrivacyAndSafetyView(TemplateView):
    template_name = 'contact_form/privacy_and_safety.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context