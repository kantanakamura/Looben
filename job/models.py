from django.db import models

from accounts.models import Users

# Create your models here.
class JobExperience(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    job_date = models.DateField()
    job_content = models.CharField(max_length=100)
    job_picture = models.FileField(blank=True, upload_to='job_experience/', default='job_experience/looben.png')