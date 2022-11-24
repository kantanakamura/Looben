from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.db.models import Prefetch
from django.http import Http404
from django.http import JsonResponse  
from django.shortcuts import get_object_or_404  


from .forms import RegistForm, UserLoginForm, AccountSettingForm, PasswordChangeForm
from .models import Schools, Users, LikeForUniversity, FollowForUser
from . import contribution_calculation
from reviews.models import ReviewOfUniversity
from questions.models import AnswerForQuestion ,Questions


class HomeView(TemplateView):
    template_name= 'accounts/home.html'
    

class RegistUserView(CreateView):
    template_name = 'accounts/regist.html'
    form_class = RegistForm
    success_message = 'アカウント作成に成功しました'
    
    def get_success_url(self):
        return reverse_lazy('accounts:user_login')   
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    authentication_form = UserLoginForm
    

class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "ログアウトに成功しました")
        return super().dispatch(request, *args, **kwargs)  
    

class AccountSettingView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/account_setting.html'
    form_class = AccountSettingForm
    model = Users
    success_message = '更新に成功しました'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_success_url(self):
        return reverse_lazy('accounts:account_setting', kwargs={'username': self.object.username})
    
    
@login_required
def password_change(request):
    password_change_form = PasswordChangeForm(request.POST or None, instance=request.user)
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            messages.success(request, 'パスワードが更新されました')
            update_session_auth_hash(request, request.user)
        except ValidationError as e:
            password_change_form.add_error('password', e)
    return render(request, 'accounts/password_change.html', context={'password_change_form': password_change_form})


@login_required
def follow_for_user_view(request):
    followed_user_pk = request.POST.get('followed_user_pk')
    context = {
        'user': f'{request.user.username}',
    }
    followed_user = get_object_or_404(Users, pk=followed_user_pk)
    follow = FollowForUser.objects.filter(followed_user=followed_user, user=request.user)
    
    if followed_user == request.user:
        Http404('自分自身はフォローできません')
    elif follow.exists():
        follow.delete()
        context['method'] = 'delete'
        context['following_message_for_javascript'] = 'フォロー'
        contribution_calculation.for_losing_follower(user=followed_user)
    else:
        follow.create(followed_user=followed_user, user=request.user)
        context['method'] = 'create'
        context['following_message_for_javascript'] = 'フォロー中'
        contribution_calculation.for_getting_follower(user=followed_user)
    context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=followed_user).count()
    return JsonResponse(context)


@login_required
def like_for_university_view(request):
    university_pk = request.POST.get('university_pk')
    context = {
        'user': f'{request.user.username}',
    }
    university = get_object_or_404(Schools, pk=university_pk)
    like = LikeForUniversity.objects.filter(target_university=university, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target_university=university, user=request.user)
        context['method'] = 'create'
    context['number_of_likes_for_university'] = university.likeforuniversity_set.count()
    return JsonResponse(context)

    
class UserRankingView(LoginRequiredMixin, ListView):
    model = Users
    template_name = 'accounts/user_ranking.html'
    ordering = ['-contributed_points']

    
class ResearchUniversity(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        high_rated_universities = Schools.objects.order_by('star_rating').reverse()[:12]
        national_universities = Schools.objects.filter(is_national=True).all()
        non_national_universities = Schools.objects.filter(is_national=False).all()
        north_universities = Schools.objects.filter(place='北部').all()
        middle_universities = Schools.objects.filter(place='中部').all()
        east_universities = Schools.objects.filter(place='東部').all()
        south_universities = Schools.objects.filter(place='南部').all()
        liked_universities = LikeForUniversity.objects.filter(user=self.request.user).all()
        if 'search' in self.request.GET:
            query = request.GET.get("search")
            universities = list(Schools.objects.all())
            searched_universities = []
            for university in universities:
                if query.capitalize() in university.name:
                    searched_universities.append(university)
            number_of_searched_universities = len(searched_universities)
            user_searched_anything = True
        else:
            searched_universities = []
            number_of_searched_universities = 0
            user_searched_anything = False
        return render(request, "accounts/research_university.html", {
            'searched_universities': searched_universities, 
            'high_rated_universities': high_rated_universities, 
            'national_universities': national_universities, 
            'non_national_universities': non_national_universities, 
            'north_universities': north_universities, 
            'middle_universities': middle_universities, 
            'east_universities': east_universities, 
            'south_universities': south_universities,
            'number_of_searched_universities': number_of_searched_universities,
            'user_searched_anything': user_searched_anything,
            'liked_universities': liked_universities,
            })
    
    
class UniversityDetailView(LoginRequiredMixin, DetailView):
    model = Schools
    template_name = 'accounts/university_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.object
        context['users'] = Users.objects.filter(school=school)[:3]
        context['reviews'] = ReviewOfUniversity.objects.filter(university=school)[:4]
        context['questions'] = Questions.objects.filter(university=school, is_solved=True).prefetch_related(
            Prefetch('answerforquestion_set', queryset=AnswerForQuestion.objects.filter(is_best_answer=True))
        )[:4]
        context['registed_students_number'] = Users.objects.filter(school=school).count()
        context['number_of_likes_for_university'] = self.object.likeforuniversity_set.count()
        if self.object.likeforuniversity_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_university'] = True
        else:
            context['is_user_liked_for_university'] = False
        school.number_of_viewer += 1
        school.save()
        return context

    
class StudentsByUniversityView(LoginRequiredMixin, DetailView):
    model = Schools
    template_name = 'accounts/students_by_university.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.object
        context['users_affiliated_with_university'] = Users.objects.filter(school=school).all()
        return context
    
        
    
class ComingSoonView(TemplateView):
    template_name = 'comingsoon.html'
    

def page_not_found(request, exception):
    return render(request, 'accounts/404.html', status=404)


def server_error(request):
    return render(request, 'accounts/500.html', status=500)