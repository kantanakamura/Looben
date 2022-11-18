from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone

from accounts.models import Users


class Blog(models.Model):
    title = models.CharField('タイトル', max_length=50)
    meta_description = models.TextField('メタデスクリプション', blank=True, max_length=150)
    content = MDTextField('テキスト', help_text='Markdown形式で書いてください。')
    top_image = models.FileField('サムネイル画像', upload_to='blog/top_image/', default='blog/top_image/top_image.png')
    created_at = models.DateField('作成日', auto_now_add=True)
    updated_at = models.DateField('更新日', auto_now=True)
    is_official = models.BooleanField(default=False)
    total_number_of_view = models.IntegerField(default=0)
    tag = models.CharField('タグ', max_length=25, null=True)
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ブログ'
        verbose_name_plural = 'ブログ'
        
        
class LikeForBlog(models.Model):
    target = models.ForeignKey(
        Blog, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        Users, on_delete=models.Model
    )
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'ブログいいね'
    

