from django.contrib import admin
#　モデルをインポート
from .models import Users, Schools, Majors, FollowForUser, LikeForUniversity


#管理ツールに登録
admin.site.register(Users)
admin.site.register(Schools)
admin.site.register(Majors)
admin.site.register(FollowForUser)
admin.site.register(LikeForUniversity)