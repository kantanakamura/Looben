from django.contrib import admin

# Register your models here.
from .models import Questions

#管理ツールに登録
admin.site.register(Questions)