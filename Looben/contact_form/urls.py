from django.urls import path
from . import views


app_name = 'contact_form'

urlpatterns = [
    path('privacy_and_safety/', views.PrivacyAndSafetyView.as_view(), name='privacy_and_safety'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
    path('contact/result/', views.ContactResultView.as_view(), name='contact_result'),
]