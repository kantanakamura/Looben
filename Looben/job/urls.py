from django.urls import path
from . import views


app_name = 'job'

urlpatterns = [
        path('create_job_experience/', views.create_job_experience, name='create_job_experience')
]