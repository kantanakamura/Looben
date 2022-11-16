from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from django.views.generic.base import View
from django.shortcuts import get_object_or_404 

from accounts.models import Users, FollowForUser
from chat.models import Messages
    
    
def get_message(request, username):
    """
    特定ユーザ間のチャット情報を取得する
    """
    conversation_partner = Users.objects.get(username=username)
    current_user = Users.objects.get(username=request.user.username)
    messages = Messages.objects.filter(sender_name=current_user.id, receiver_name=conversation_partner.id) | \
               Messages.objects.filter(sender_name=conversation_partner.id, receiver_name=current_user.id)
    amount_of_following_users = FollowForUser.objects.filter(user=request.user).count()
    following_user_list =  FollowForUser.objects.filter(user=request.user)
    for message in messages:
        if message.sender_name == conversation_partner:
            message.seen = True
            message.save()
    return render(request, "chat/messages.html", {
        'messages': messages,
        'following_user_list': following_user_list,
        'current_user': current_user, 
        'conversation_partner': conversation_partner,
        'amount_of_following_users': amount_of_following_users,
        })
    
    
def follow_and_create_chatroom(request, username):
    followed_user = get_object_or_404(Users, username=username)
    follow = FollowForUser.objects.filter(followed_user=followed_user, user=request.user)

    if not follow.exists():
        follow.create(followed_user=followed_user, user=request.user)
    messages = Messages.objects.filter(sender_name=followed_user.id, receiver_name=request.user.id) | \
        Messages.objects.filter(sender_name=request.user.id, receiver_name=followed_user.id)
    amount_of_following_users = FollowForUser.objects.filter(user=request.user).count()
    following_user_list =  FollowForUser.objects.filter(user=request.user)
    return redirect("chat:get_message", username=username)
    
    
class ChatRoomView(DetailView):
    template_name = 'chat/chat_room.html' 
    model = Users
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['following_user_list'] = FollowForUser.objects.filter(user=user)
        context['amount_of_following_users'] = FollowForUser.objects.filter(user=user).count()
        return context
        
        
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
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        for message in messages:
            message.seen = True
            message.save()
        serializer = MessageSerializer(instance=messages, many=True)
        return JsonResponse(serializer.data, safe=False)