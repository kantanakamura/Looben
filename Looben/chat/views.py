from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import get_object_or_404 
from django.http import Http404

from .models import ConversationPartner
from accounts.models import Users, FollowForUser
from chat.models import Messages
from notifications.models import Notification
    
    
def get_message(request, username):
    """
    特定ユーザ間のチャット情報を取得する
    """
    conversation_partner = get_object_or_404(Users, username=username)
    current_user = get_object_or_404(Users, username=request.user.username)
    if conversation_partner == current_user:
        Http404("自分自身とはチャットできません")
    messages = Messages.objects.filter(sender_name=current_user.id, receiver_name=conversation_partner.id) | \
               Messages.objects.filter(sender_name=conversation_partner.id, receiver_name=current_user.id)
    number_of_conversation_partners = ConversationPartner.objects.filter(current_user=request.user).count()
    conversation_partner_list =  ConversationPartner.objects.filter(current_user=request.user).order_by('timestamp').reverse()
    notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
    number_of_notification =  Notification.objects.filter(receiver=request.user).count()
    has_notifications =  Notification.objects.filter(receiver=request.user).exists()
    for message in messages:
        if message.sender_name == conversation_partner:
            message.is_seen = True
            message.save()
    return render(request, "chat/messages.html", {
        'messages': messages,
        'conversation_partner_list': conversation_partner_list,
        'current_user': current_user, 
        'conversation_partner': conversation_partner,
        'number_of_conversation_partners': number_of_conversation_partners,
        'notification_lists': notification_lists,
        'number_of_notification': number_of_notification,
        'has_notifications': has_notifications
        })
    
    
def create_chatroom(request, username):
    conversation_partner = get_object_or_404(Users, username=username)
    conversation_connectoin = ConversationPartner.objects.filter(conversation_partner=conversation_partner, current_user=request.user)
    if conversation_partner == request.user:
        Http404("自分自身とチャットはできません")
    elif not conversation_connectoin.exists():
        conversation_connectoin.create(conversation_partner=conversation_partner, current_user=request.user)
        ConversationPartner(conversation_partner=request.user, current_user=conversation_partner)
    return redirect("chat:get_message", username=username)
    
    
class ChatRoomView(LoginRequiredMixin, View):
    template_name = 'chat/chat_room.html' 
    model = Users
    
    def get(self, request,  *args, **kwargs):
        user = request.user
        number_of_conversation_partners = ConversationPartner.objects.filter(current_user=request.user).count()
        conversation_partner_list =  ConversationPartner.objects.filter(current_user=request.user).order_by('timestamp').reverse()
        if 'search' in self.request.GET:
            keyword_query = request.GET.get('search')
            if keyword_query == '':
                searched_users = []
                number_of_searched_users = 0
                user_searched_anything = False
            else:
                users = conversation_partner_list
                searched_users = []
                for user in users:
                    if keyword_query in user.conversation_partner.name:
                        searched_users.append(user.conversation_partner)
                number_of_searched_users = len(searched_users)
                user_searched_anything = True
        else:
            searched_users = []
            number_of_searched_users = 0
            user_searched_anything = False
        notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
        number_of_notification =  Notification.objects.filter(receiver=request.user).count()
        has_notifications =  Notification.objects.filter(receiver=request.user).exists()
        return render(request, 'chat/chat_room.html', {
            'conversation_partner_list': conversation_partner_list,
            'number_of_conversation_partners': number_of_conversation_partners,
            'searched_users': searched_users,
            'user_searched_anything': user_searched_anything,
            'number_of_searched_users': number_of_searched_users,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications
            })
        
        
class UpdateMessage(View):

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)
    
    def get(self, request, *args, **kwargs):
        sender = self.kwargs.get('sender')
        receiver =  self.kwargs.get('receiver')
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, is_seen=False)
        for message in messages:
            message.is_seen = True
            message.save()
        serializer = MessageSerializer(instance=messages, many=True)
        return JsonResponse(serializer.data, safe=False)