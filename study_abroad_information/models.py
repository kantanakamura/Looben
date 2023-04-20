from django.db import models
from django.utils import timezone

from accounts.models import Users


class StudyAbroadInformation(models.Model):
    title = models.CharField('タイトル', max_length=50)
    meta_description = models.TextField('メタデスクリプション', blank=True, max_length=150)
    url = models.CharField('url', max_length=600, default='#')
    top_image = models.FileField('サムネイル画像', upload_to='information/', default='blog/top_image/top_image.png')
    created_at = models.DateField('作成日', default=timezone.now)
    is_official = models.BooleanField(default=False)
    tag = models.CharField('タグ', max_length=25, null=True)
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '留学情報投稿'
        verbose_name_plural = '留学情報投稿'