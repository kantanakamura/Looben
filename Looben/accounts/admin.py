from django.contrib import admin
#　モデルをインポート
from .models import Users, Schools, Majors


#管理ツールに登録
admin.site.register(Users)
admin.site.register(Schools)
admin.site.register(Majors)