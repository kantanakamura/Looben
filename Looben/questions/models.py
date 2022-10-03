from unicodedata import category
from django.db import models
from django.utils import timezone

from accounts.models import Users, Schools


class Questions(models.Model):
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, default='未記入')
    is_solved = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    university = models.ForeignKey(
        Schools, on_delete=models.CASCADE, null=True
    )
    
    class Meta:
        db_table = 'questions'
        verbose_name_plural = '質問'
        
    def __str__(self):
        return str(self.user)
    
    
class AnswerForQuestion(models.Model):
    answer = models.TextField(max_length=500)
    is_best_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'answer_for_question'
        verbose_name_plural = '質問回答'
        
    def __str__(self):
        return str(self.user)