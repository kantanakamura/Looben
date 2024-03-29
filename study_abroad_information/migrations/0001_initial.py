# Generated by Django 4.0.6 on 2023-02-08 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyAbroadInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='タイトル')),
                ('meta_description', models.TextField(blank=True, max_length=150, verbose_name='メタデスクリプション')),
                ('url', models.CharField(default='#', max_length=600, verbose_name='url')),
                ('top_image', models.FileField(default='blog/top_image/top_image.png', upload_to='blog/top_image/', verbose_name='サムネイル画像')),
                ('created_at', models.DateField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('is_official', models.BooleanField(default=False)),
                ('tag', models.CharField(max_length=25, null=True, verbose_name='タグ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '留学情報投稿',
                'verbose_name_plural': '留学情報投稿',
            },
        ),
    ]
