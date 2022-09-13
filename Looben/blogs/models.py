from django.db import models
from django.utils.html import mark_safe
from markdown import markdown

from accounts.models import Users


class Blog(models.Model):
    title = models.CharField('タイトル', max_length=50)
    content = models.TextField('テキスト')
    top_image = models.FileField('サムネイル画像', upload_to='blog/top_image/', default='blog/top_image/top_image.png')
    created_at = models.DateField('作成日', auto_now_add=True)
    updated_at = models.DateField('更新日', auto_now=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ブログ'
        verbose_name_plural = 'ブログ'
        
    def get_content_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))
    