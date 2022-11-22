from django.urls import path
from . import views


app_name = 'job'

urlpatterns = [
        path('create_job_experience/', views.create_job_experience, name='create_job_experience'),
        path('update_job_experience/<int:pk>', views.UpdateJobExperienceView.as_view(), name='update_job_experience'),
        path('delete_job_experience/<int:pk>', views.DeleteJobExperienceView.as_view(), name='delete_job_experience'),
]