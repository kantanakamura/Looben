from multiprocessing import connection
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.db.models import Q, Prefetch


from .forms import RegistForm, UserLoginForm, AccountSettingForm, PasswordChangeForm
from .models import Schools, Users, LikeForUniversity
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
def connect_view(request, *args, **kwargs):
    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        follower = Users.objects.get(username=request.user.username)
        #kwargs['username'] = フォロー対象のユーザー名を渡す。
        following = Users.objects.get(username=kwargs['username'])
        #例外処理：もしフォロー対象が存在しない場合、警告文を表示させる。
    except Users.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': following.username}))
    #フォローしようとしている対象が自分の場合、警告文を表示させる。
    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
        return HttpResponseRedirect(reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': following.username}))
    else:
        #フォロー対象をまだフォローしていなければ、DBにフォロワー(自分)×フォロー(相手)という組み合わせで登録する。
        #alreadyにはTrueが入る
        already_connected = follower.connection.filter(id=following.id)

    #もしcreatedがTrueの場合、フォロー完了のメッセージを表示させる。
    if not already_connected:
        follower.connection.add(following)
        messages.success(request, '{}をフォローしました'.format(following.username))
        #既にフォロー相手をフォローしていた場合、already_connectedにはFalseが入る。
    else:
        #フォロー済みのメッセージを表示させる。
        messages.warning(request, 'あなたはすでに{}をフォローしています'.format(following.username))
    return HttpResponseRedirect(reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': following.username}))


@login_required
def disconnect_view(request, *args, **kwargs):
    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        follower = Users.objects.get(username=request.user.username)
        #kwargs['username'] = フォロー対象のユーザー名を渡す。
        following = Users.objects.get(username=kwargs['username'])
        #例外処理：もしフォロー対象が存在しない場合、警告文を表示させる。
    except Users.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': following.username}))
        
    #フォロー対象をすでにフォローしていれば、DBにフォロワー(自分)×フォロー(相手)という組み合わを削除する。
    #alreadyにはTrueが入る
    already_connected = follower.connection.filter(id=following.id)
    #もしcreatedがTrueの場合、フォロー解除完了のメッセージを表示させる。
    if already_connected:
        follower.connection.remove(following)
        messages.success(request, '{}のフォロー解除をしました'.format(following.username))
        #まだフォロー相手をフォローしていなかった場合、already_connectedにはFalseが入る。
    else:
        #未フォローのメッセージを表示させる。
        messages.warning(request, 'あなたはまだ{}をフォローしていません'.format(following.username))
    return HttpResponseRedirect(reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': following.username}))


@login_required
def save_users_view(request, *args, **kwargs):
    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        saver = Users.objects.get(username=request.user.username)
        #kwargs['username'] = 保存対象のユーザー名を渡す。
        saved_user = Users.objects.get(username=kwargs['username'])
        #例外処理：もし保存対象が存在しない場合、警告文を表示させる。
    except Users.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('accounts:user_ranking'))
    #保存しようとしている対象が自分の場合、警告文を表示させる。
    if saver == saved_user:
        messages.warning(request, '自分自身は保存できません')
        return HttpResponseRedirect(reverse_lazy('accounts:user_ranking'))
    else:
        #保存対象をまだ保存していなければ、DBに保存しようとしてる人(自分)×保存対象(相手)という組み合わせで登録する。
        #alreadyにはTrueが入る
        already_saved = saver.saved_users.filter(username=saved_user.username)

    #もしalready_savedがFalseの場合、保存完了のメッセージを表示させる。
    if not already_saved:
        saver.saved_users.add(saved_user)
        messages.success(request, '{}を保存しました'.format(saved_user.username))
        #既に保存相手を保存していた場合、already_savedにはFalseが入る。
    else:
        #保存済みのメッセージを表示させる。
        messages.warning(request, 'あなたはすでに{}を保存しています'.format(saved_user.username))
    return HttpResponseRedirect(reverse_lazy('accounts:user_ranking'))


@login_required
def unsave_users_view(request, *args, **kwargs):
    try:
        saver = Users.objects.get(username=request.user.username)
        saved_user = Users.objects.get(username=kwargs['username'])
        if saver == saved_user:
            messages.warning(request, '自分自身の保存を解除できません')
        else:
            #保存しようとしている人(自分)×保存される人(相手)という組み合わせを削除する。
            saver.saved_users.remove(saved_user)
            messages.success(request, 'あなたは{}の保存を解除しました'.format(saved_user.username))
    except Users.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('accounts:user_ranking'))
    except Users.DoesNotExist:
        messages.warning(request, 'あなたは{}を保存しませんでした'.format(saved_user.username))

    return HttpResponseRedirect(reverse_lazy('accounts:user_ranking'))


@login_required
def save_university_view(request, *args, **kwargs):
    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        saver = Users.objects.get(username=request.user.username)
        #kwargs['username'] = 保存対象のユーザー名を渡す。
        saved_university = Schools.objects.get(id=kwargs['school_id'])
        #例外処理：もし保存対象が存在しない場合、警告文を表示させる。
    except Users.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['school_id']))
        return HttpResponseRedirect(reverse_lazy('accounts:reseach_university'))
    #保存対象をまだ保存していなければ、DBに保存しようとしてる人(自分)×保存対象(相手)という組み合わせで登録する。
    #alreadyにはTrueが入る
    already_saved = saver.saved_university.filter(name=saved_university.name)

    #もしalready_savedがFalseの場合、保存完了のメッセージを表示させる。
    if not already_saved:
        saver.saved_university.add(saved_university)
        messages.success(request, '{}を保存しました'.format(saved_university.name))
        #既に保存相手を保存していた場合、already_savedにはFalseが入る。
    else:
        #保存済みのメッセージを表示させる。
        messages.warning(request, 'あなたはすでに{}を保存しています'.format(saved_university.name))
    return HttpResponseRedirect(reverse_lazy('accounts:research_university'))


@login_required
def unsave_university_view(request, *args, **kwargs):
    try:
        saver = Users.objects.get(username=request.user.username)
        saved_university = Schools.objects.get(id=kwargs['school_id'])
        #保存しようとしている人(自分)×保存される人(相手)という組み合わせを削除する。
        saver.saved_university.remove(saved_university)
        messages.success(request, 'あなたは{}の保存を解除しました'.format(saved_university.name))
    except Users.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(saved_university.name))
        return HttpResponseRedirect(reverse_lazy('accounts:research_university'))
    except Users.DoesNotExist:
        messages.warning(request, 'あなたは{}を保存しませんでした'.format(saved_university.name))
    return HttpResponseRedirect(reverse_lazy('accounts:research_university'))


def page_not_found(request, exception):
    return render(request, 'accounts/404.html', status=404)


def server_error(request):
    return render(request, 'accounts/500.html', status=500)
    
    
class UserRankingView(LoginRequiredMixin, ListView):
    model = Users
    template_name = 'accounts/user_ranking.html'
    ordering = ['-contributed_points']
    
    
class ResearchUniversity(View):
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
        if self.object.likeforuniversity_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_university'] = True
        else:
            context['is_user_liked_for_university'] = False
        school.number_of_viewer += 1
        school.save()
        return context

    
class StudentsByUniversityView(LoginRequiredMixin, ListView):
    model = Users
    template_name = 'accounts/students_by_university.html'
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        id = self.request.GET.get('id')
        if id is not None:
            queryset = queryset.filter(school__id=id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.GET.get('id')
        if id is not None:
            context['school'] = Schools.objects.filter(id=id)
        return context
        
    
class ComingSoonView(TemplateView):
    template_name = 'comingsoon.html'
    