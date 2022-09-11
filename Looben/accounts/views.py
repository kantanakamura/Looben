import email
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


from .forms import RegistForm, UserLoginForm, AccountSettingForm, PasswordChangeForm
from .models import Schools, Users
from reviews.models import ReviewOfUniversity


#　ホーム画面
class HomeView(TemplateView):
    template_name= 'accounts/home.html'
    

#　アカウント作成画面
class RegistUserView(CreateView):
    template_name = 'accounts/regist.html'
    form_class = RegistForm
    success_message = 'アカウント作成に成功しました'
    
    def get_success_url(self):
        return reverse_lazy('accounts:user_login')   
    
    # def post(self, request, *args, **kwargs):
    #     form = RegistForm(request.POST or None)
    #     if form.is_valid():
    #         form.save()
    #         user = authenticate(email=self.request.POST['email'], password=self.request.POST['password'])
    #         login(self.request, user)
    #         return redirect('accounts:research_university')

# ユーザーのログイン
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    authentication_form = UserLoginForm
    

# ユーザーのログアウト
class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "ログアウトに成功しました")
        return super().dispatch(request, *args, **kwargs)  
    

# アカウントの詳細設定
class AccountSettingView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/account_setting.html'
    form_class = AccountSettingForm
    model = Users
    success_message = '更新に成功しました'
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'username'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'username'
    
    def get_success_url(self):
        return reverse_lazy('accounts:account_setting', kwargs={'username': self.object.username})
    
    

#　ユーザーのパスワード変更画面
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
    return HttpResponseRedirect(reverse_lazy('accounts:university_detail', kwargs={'pk': saved_university.id}))


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
    
     
class ResearchUniversity(ListView):
    model = Schools
    template_name = 'accounts/research_university.html'    
    
    
class UniversityDetailView(DetailView):
    model = Schools
    template_name = 'accounts/university_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.object
        # この大学の在学生のアカウントを3つ取得
        context['users'] = Users.objects.filter(school=school)[:3]
        # この大学のレビューを4つ取得
        context['reviews'] = ReviewOfUniversity.objects.filter(university=school)[:4]
        # Loobenにアカウント登録してる、この大学の在学生の数を取得
        registed_students_number = Users.objects.filter(school=school).count()
        context['registed_students_number'] = registed_students_number
        # 詳細ページを訪れた人の数を１増やす
        school.number_of_viewer += 1
        school.save()
        return context
     
    
class StudentsByUniversityView(LoginRequiredMixin, ListView):
    model = Users
    template_name = 'accounts/students_by_university.html'
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) # Users.objects.all() と同じ結果
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
    
        
class MessageView(TemplateView):
    template_name = 'accounts/messaging.html'     
    
    
class ComingSoonView(TemplateView):
    template_name = 'comingsoon.html'
    