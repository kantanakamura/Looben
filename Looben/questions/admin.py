from django.contrib import admin

# Register your models here.
from .models import Questions, AnswerForQuestion

#管理ツールに登録
admin.site.register(Questions)
admin.site.register(AnswerForQuestion)