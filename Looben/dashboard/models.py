from django.db import models
from django.utils import timezone

from accounts.models import Users

# Create your models here.
class Post(models.Model):
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'post'
        verbose_name_plural = '投稿'
        
    def __str__(self):
        return str(self.user)
    