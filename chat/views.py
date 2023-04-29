from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.shortcuts import get_object_or_404 
from django.http import Http404

from .models import ConversationPartner
from accounts.models import Users
from chat.models import Messages
from notifications.models import Notification
    

@login_required
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
    have_new_message_conversation_partner_list =  ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).order_by('timestamp').reverse()
    no_new_message_conversation_partner_list =  ConversationPartner.objects.filter(current_user=request.user, have_new_message=False).order_by('timestamp').reverse()
    notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
    number_of_notification =  Notification.objects.filter(receiver=request.user).count()
    has_notifications =  Notification.objects.filter(receiver=request.user).exists()
    has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
    for message in messages:
        if message.sender_name == conversation_partner:
            message.is_seen = True
            message.save()
    ConversationPartner.objects.filter(current_user=current_user, conversation_partner=conversation_partner).update(have_new_message=False)
    return render(request, "chat/messages.html", {
        'messages': messages,
        'have_new_message_conversation_partner_list': have_new_message_conversation_partner_list,
        'no_new_message_conversation_partner_list': no_new_message_conversation_partner_list,
        'current_user': current_user, 
        'conversation_partner': conversation_partner,
        'number_of_conversation_partners': number_of_conversation_partners,
        'notification_lists': notification_lists,
        'number_of_notification': number_of_notification,
        'has_notifications': has_notifications,
        'has_not_seen_message': has_not_seen_message
        })
    
@login_required
def create_chatroom(request, username):
    conversation_partner = get_object_or_404(Users, username=username)
    conversation_connection = ConversationPartner.objects.filter(conversation_partner=conversation_partner, current_user=request.user)
    conversation_connection_for_other = ConversationPartner.objects.filter(conversation_partner=request.user, current_user=conversation_partner)
    if conversation_partner == request.user:
        Http404("自分自身とチャットはできません")
    elif not conversation_connection.exists():
        conversation_connection.create(conversation_partner=conversation_partner, current_user=request.user)
        conversation_connection_for_other.create(conversation_partner=request.user, current_user=conversation_partner)
    return redirect("chat:get_message", username=username)
    
    
class ChatRoomView(LoginRequiredMixin, View):
    template_name = 'chat/chat_room.html' 
    model = Users
    
    def get(self, request,  *args, **kwargs):
        user = request.user
        number_of_conversation_partners = ConversationPartner.objects.filter(current_user=user).count()
        have_new_message_conversation_partner_list =  ConversationPartner.objects.filter(current_user=user, have_new_message=True).order_by('timestamp').reverse()
        no_new_message_conversation_partner_list =  ConversationPartner.objects.filter(current_user=user, have_new_message=False).order_by('timestamp').reverse()
        has_not_seen_message = ConversationPartner.objects.filter(current_user=user, have_new_message=True).exists()
        if 'search' in self.request.GET:
            keyword_query = request.GET.get('search')
            if keyword_query == '':
                searched_have_new_message_users = []
                searched_no_new_message_users = []
                user_searched_anything = False
            else:
                have_new_message_users = have_new_message_conversation_partner_list
                no_new_message_users = no_new_message_conversation_partner_list
                searched_have_new_message_users = []
                searched_no_new_message_users = []
                for user in have_new_message_users:
                    if keyword_query in user.conversation_partner.name:
                        searched_have_new_message_users.append(user.conversation_partner)
                for user in no_new_message_users:
                    if keyword_query in user.conversation_partner.name:
                        searched_no_new_message_users.append(user.conversation_partner)
                user_searched_anything = True
        else:
            searched_have_new_message_users = []
            searched_no_new_message_users = []
            user_searched_anything = False
        notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
        number_of_notification =  Notification.objects.filter(receiver=request.user).count()
        has_notifications =  Notification.objects.filter(receiver=request.user).exists()
        return render(request, 'chat/chat_room.html', {
            'have_new_message_conversation_partner_list': have_new_message_conversation_partner_list,
            'no_new_message_conversation_partner_list': no_new_message_conversation_partner_list,
            'number_of_conversation_partners': number_of_conversation_partners,
            'searched_have_new_message_users': searched_have_new_message_users,
            'searched_no_new_message_users': searched_no_new_message_users,
            'user_searched_anything': user_searched_anything,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
            })
        
        
class UpdateMessage(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        conversation_partner = self.kwargs.get('sender')
        current_user =  self.kwargs.get('receiver')
        
        if serializer.is_valid():
            serializer.save()
            ConversationPartner.objects.filter(current_user=conversation_partner, conversation_partner=current_user).update(have_new_message=True)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    def get(self, request, *args, **kwargs):
        conversation_partner = self.kwargs.get('sender')
        current_user =  self.kwargs.get('receiver')
        messages = Messages.objects.filter(sender_name=conversation_partner, receiver_name=current_user, is_seen=False)
        ConversationPartner.objects.filter(current_user=current_user, conversation_partner=conversation_partner).update(have_new_message=False)
        for message in messages:
            message.is_seen = True
            message.save()
        serializer = MessageSerializer(instance=messages, many=True)
        return JsonResponse(serializer.data, safe=False)