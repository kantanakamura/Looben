from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/<str:username>', views.get_message, name='get_message'),
    path('chat_room/', views.ChatRoomView.as_view(), name='chat_room'),  
    path('api/messages', views.UpdateMessage.as_view()),
    path('api/messages/<int:sender>/<int:receiver>', views.UpdateMessage.as_view()), 
    path('follow_and_create_chatroom/<str:username>', views.follow_and_create_chatroom, name='follow_and_crete_chatroom')
]