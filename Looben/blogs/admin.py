from django.contrib import admin

# Register your models here.
#　モデルをインポート
from .models import Blog


#管理ツールに登録
admin.site.register(Blog)
