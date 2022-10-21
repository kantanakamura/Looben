from django.shortcuts import render
from django.views.generic.detail import DetailView


from accounts.models import Users
from chat.models import Messages


def getFriendsList(username):
    try:
        user = Users.objects.get(username=username)
        friends = list(user.connection.all())
        return friends
    except:
        return []
    
    
def get_message(request, username):
    """
    特定ユーザ間のチャット情報を取得する
    """
    friend = Users.objects.get(username=username)
    current_user = Users.objects.get(username=request.user.username)
    messages = Messages.objects.filter(sender_name=current_user.id, receiver_name=friend.id) | \
               Messages.objects.filter(sender_name=friend.id, receiver_name=current_user.id)
    friends_list = getFriendsList(request.user.username)
    return render(request, "chat/messages.html", {
        'messages': messages,
        'friends_list': friends_list,
        'current_user': current_user, 
        'friend': friend
        })
    
    
class ChatRoomView(DetailView):
    template_name = 'chat/chat_room.html' 
    model = Users
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['friends_list'] = getFriendsList(user.username)
        context['amount_of_friends'] = user.connection.all().count()
        return context