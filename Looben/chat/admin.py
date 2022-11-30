from django.contrib import admin
from .models import Messages, ConversationPartner


class MessagesAdmin(admin.ModelAdmin):
    list_display=('pk','description','sender_name', 'receiver_name','time', 'is_seen', 'timestamp')


admin.site.register(Messages, MessagesAdmin)
admin.site.register(ConversationPartner)