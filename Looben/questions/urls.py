from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('question/', views.QuestionView.as_view(), name='question'),
]