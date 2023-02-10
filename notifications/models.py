from django.db import models
from django.utils import timezone

from accounts.models import Users

# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='send_user')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE,  related_name='receive_user')
    message = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'notification'
        verbose_name = '通知'
        
    def __str__(self):
        return str(self.sender) + ' ' + str(self.receiver) + ' ' + str(self.timestamp)