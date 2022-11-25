from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import get_object_or_404 
from django.http import Http404

from accounts.models import Users, FollowForUser
from chat.models import Messages
    
    
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

    if followed_user == request.user:
        Http404("自分自身とチャットはできません")
    elif not follow.exists():
        follow.create(followed_user=followed_user, user=request.user)
    return redirect("chat:get_message", username=username)
    
    
class ChatRoomView(LoginRequiredMixin, View):
    template_name = 'chat/chat_room.html' 
    model = Users
    
    def get(self, request,  *args, **kwargs):
        user = request.user
        following_user_list = FollowForUser.objects.filter(user=user)
        amount_of_following_users = FollowForUser.objects.filter(user=user).count()
        if 'search' in self.request.GET:
            keyword_query = request.GET.get('search')
            if keyword_query == '':
                searched_users = []
                number_of_searched_users = 0
                user_searched_anything = False
            else:
                users = following_user_list
                searched_users = []
                for user in users:
                    if keyword_query in user.followed_user.name:
                        searched_users.append(user.followed_user)
                number_of_searched_users = len(searched_users)
                user_searched_anything = True
        else:
            searched_users = []
            number_of_searched_users = 0
            user_searched_anything = False
        return render(request, 'chat/chat_room.html', {
            'following_user_list': following_user_list,
            'amount_of_following_users': amount_of_following_users,
            'searched_users': searched_users,
            'user_searched_anything': user_searched_anything,
            'number_of_searched_users': number_of_searched_users,
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
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        for message in messages:
            message.seen = True
            message.save()
        serializer = MessageSerializer(instance=messages, many=True)
        return JsonResponse(serializer.data, safe=False)