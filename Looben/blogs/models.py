from email.policy import default
from django.db import models
from mdeditor.fields import MDTextField
from accounts.models import Users


class Blog(models.Model):
    title = models.CharField('タイトル', max_length=50)
    content = MDTextField('テキスト', help_text='Markdown形式で書いてください。')
    top_image = models.FileField('サムネイル画像', upload_to='blog/top_image/', default='blog/top_image/top_image.png')
    created_at = models.DateField('作成日', auto_now_add=True)
    updated_at = models.DateField('更新日', auto_now=True)
    is_official = models.BooleanField(default=False)
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
    
    class Meta:
        verbose_name = 'ブログいいね'
    