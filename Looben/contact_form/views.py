from django.shortcuts import render
from django.views.generic.base import TemplateView


class PrivacyAndSafetyView(TemplateView):
    template_name = 'contact_form/privacy_and_safety.html'