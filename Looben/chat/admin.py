from django.contrib import admin
from .models import Messages


class MessagesAdmin(admin.ModelAdmin):
    list_display=('pk','description','sender_name', 'receiver_name','time', 'seen', 'timestamp')


admin.site.register(Messages, MessagesAdmin)