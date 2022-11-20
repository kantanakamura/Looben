from django.views.generic.detail import DetailView

from accounts.models import Users, FollowForUser
from blogs.models import Blog
from reviews.models import ReviewOfUniversity
from job.models import JobExperience


class PostInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/post_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['blog_posts'] = Blog.objects.filter(author=user).all()
        context['job_experiences'] = JobExperience.objects.filter(user=user).all()
        context['newest_users_list'] = Users.objects.filter(state='現役台湾留学生').order_by('joined_at').reverse()[:4]
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
    
    
class ReviewInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/review_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['reviews'] = ReviewOfUniversity.objects.filter(user=user).all()
        context['job_experiences'] = JobExperience.objects.filter(user=user).all()
        context['newest_users_list'] = Users.objects.filter(state='現役台湾留学生').order_by('joined_at').reverse()[:4]
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
    

class FollowingInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/following_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['job_experiences'] = JobExperience.objects.filter(user=user).all()
        context['newest_users_list'] = Users.objects.filter(state='現役台湾留学生').order_by('joined_at').reverse()[:4]
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
    
    
class FollowedInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/followed_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['job_experiences'] = JobExperience.objects.filter(user=user).all()
        context['newest_users_list'] = Users.objects.filter(state='現役台湾留学生').order_by('joined_at').reverse()[:4]
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context

    
class QuestionInDashboardView(DetailView):
    model = Users
    template_name = 'dashboard/question_in_dashboard.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['asked_questions'] = user.questions_set.filter(is_anonymous=False).all()
        context['job_experiences'] = JobExperience.objects.filter(user=user).all()
        context['newest_users_list'] = Users.objects.filter(state='現役台湾留学生').order_by('joined_at').reverse()[:4]
        context['is_user_following'] = FollowForUser.objects.filter(user=self.request.user, followed_user=user).exists()
        if context['is_user_following']:
            context['following_message_for_javascript'] = 'フォロー中'
        else:
            context['following_message_for_javascript'] = 'フォロー'
        return context
