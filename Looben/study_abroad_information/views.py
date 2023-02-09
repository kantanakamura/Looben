from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404 

from .forms import CreateInformationPostForm, EditInformationPostForm
from .models import StudyAbroadInformation
from accounts.models import FollowForUser
from accounts import contribution_calculation
from notifications.models import Notification
from chat.models import ConversationPartner


class CheckForUserMatchMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        target_information_post = get_object_or_404(StudyAbroadInformation, pk=self.kwargs['pk'])
        return self.request.user == target_information_post.author
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Only user who made this author have access to this view'}
        )
        

@login_required
def create_information_post(request):
    create_information_post_form = CreateInformationPostForm(request.POST or None)
    if create_information_post_form.is_valid():
        create_information_post_form.instance.author = request.user
        create_information_post_form.save()
        contribution_calculation.for_creating_post(author=request.user)
        # フォロワーへの留学情報作成の通知を作成
        for follow in FollowForUser.objects.filter(followed_user=request.user).all():
            create_information_post_notification = Notification(sender=request.user, receiver=follow.user, message= str(request.user.username) + 'が新しく留学情報を投稿しました。')
            create_information_post_notification.save()
        return redirect('study_abroad_information:information_post_list')
    notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
    number_of_notification =  Notification.objects.filter(receiver=request.user).count()
    has_notifications =  Notification.objects.filter(receiver=request.user).exists()
    has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
    return render(
        request, 'study_abroad_information/create_information_post.html', context={
            'create_information_post_form': create_information_post_form,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
        }
    )
    
    
class DeleteInformationPostView(CheckForUserMatchMixin, DeleteView):
    template_name = 'study_abroad_information/delete_information_post.html'
    model = StudyAbroadInformation
    
    def get_success_url(self):
        return reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': self.object.author.username}) 
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context
    

class EditInformationPostView(CheckForUserMatchMixin, UpdateView):
    template_name = 'study_abroad_information/edit_information_post.html'
    form_class = EditInformationPostForm
    model = StudyAbroadInformation
    
    def get_success_url(self):
        return reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': self.object.author.username}) 
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context
    
    
class InformationPostListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        number_of_following_user = FollowForUser.objects.filter(user=user).count()
        number_of_followed_user = FollowForUser.objects.filter(followed_user=user).count()
        number_of_information_post = StudyAbroadInformation.objects.filter(author=user).count()
        newest_information_posts = StudyAbroadInformation.objects.filter(is_official=False).order_by('-created_at')[:6]
        official_information_post_lists = StudyAbroadInformation.objects.filter(is_official=True).order_by('-created_at')[:3]
        notification_lists =  Notification.objects.filter(receiver=user).order_by('timestamp').reverse()[:3]
        number_of_notification =  Notification.objects.filter(receiver=user).count()
        has_notifications =  Notification.objects.filter(receiver=user).exists()
        has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
        if 'search' in self.request.GET:
            keyword_query = request.GET.get('search')
            if keyword_query == '':
                searched_posts = []
                number_of_searched_posts = 0
                user_searched_something = False
            else:
                posts = list(StudyAbroadInformation.objects.all())
                searched_posts = []
                for post in posts:
                    if keyword_query in post.meta_description:
                        searched_posts.append(post)
                number_of_searched_posts = len(searched_posts)
                user_searched_something = True
        else:
            searched_posts = []
            number_of_searched_posts = 0
            user_searched_something = False
        return render(request, 'study_abroad_information/information_post_list.html', {
            'number_of_following_user': number_of_following_user,
            'number_of_followed_user': number_of_followed_user,
            'number_of_information_post': number_of_information_post,
            'newest_information_posts': newest_information_posts,
            'official_information_post_lists': official_information_post_lists,
            'number_of_searched_posts': number_of_searched_posts,
            'user_searched_something': user_searched_something,
            'searched_posts': searched_posts,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
            })
    
    
class InOrderInformationPostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        information_posts_order_by_date = StudyAbroadInformation.objects.filter(is_official=False).order_by('-created_at')[:30]
        official_information_post_lists = StudyAbroadInformation.objects.filter(is_official=True).order_by('-created_at')[:30]
        notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
        number_of_notification =  Notification.objects.filter(receiver=request.user).count()
        has_notifications =  Notification.objects.filter(receiver=request.user).exists()
        has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
        return render(request, 'study_abroad_information/in_order_information_post.html', {
            'information_posts_order_by_date': information_posts_order_by_date,
            'official_information_post_lists': official_information_post_lists,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
            })