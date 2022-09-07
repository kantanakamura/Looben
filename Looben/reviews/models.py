from django.db import models
from accounts.models import Schools, Users


class ReviewOfUniverity(models.Model):
    title = models.CharField(max_length=100)
    review = models.TextField(max_length=300)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    university = models.ForeignKey(
        Schools, on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'review_of_university'
        verbose_name_plural = '口コミ'
        
    def __str__(self):
        return self.title + ' : ' + str(self.user)