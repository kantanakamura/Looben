from multiprocessing import connection
from tkinter.messagebox import QUESTION
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

from .forms import QuestionForm, AnswerForQuestionForm
from .models import Questions, AnswerForQuestion

from accounts.models import Schools


class QuestionView(ListView):
    template_name = 'question/question.html'
    model = Questions
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 回答募集中の質問を4つ取得
        context['question_seeking_answers'] = Questions.objects.filter(is_solved=False).all()[:4]  
        # 最新の解決済みの質問を4つ取得  
        context['solved_questions'] = Questions.objects.filter(is_solved=True).prefetch_related(
            Prefetch('answerforquestion_set', queryset=AnswerForQuestion.objects.filter(is_best_answer=True))
        )[:4]
        
        return context
    
    
@login_required
def ask_question(request):
    ask_question_form = QuestionForm(request.POST or None)
    if ask_question_form.is_valid():
        ask_question_form.instance.user = request.user
        if ask_question_form['is_anonymous'] == 'on':
            ask_question_form.instance.is_anonymous = True
        else:
            ask_question_form.instance.is_anonymous = False
        ask_question_form.save()
        return redirect('questions:question')
    return render(
        request, 'question/ask_question.html', context={
            'ask_question_form': ask_question_form
        }
    )
    
    
class QuestionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'question/question_detail.html'
    model = Questions
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 質問に対する回答の数
        context['number_of_answer'] = self.object.answerforquestion_set.all().count()
        context['best_answer'] = self.object.answerforquestion_set.filter(is_best_answer=True).first()
        context['form'] = AnswerForQuestionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AnswerForQuestionForm(request.POST or None)
        if form.is_valid():
            form.instance.question = self.object
            form.instance.user = request.user
            form.save()
            return redirect('questions:question_detail', pk=self.object.id)
        else:
            context = self.get_context_data()
            context['form'] = form  # form.is_validしたフォームを渡さないと、フォームのエラーを表示できない
            return render(request, 'questions:question_detail', context)
    
    
class CategorizedQuestionsView(DetailView):
    model = Questions
    template_name = 'question/categorized_questions.html'
    
    #slug_field = urls.pyに渡すモデルのフィールド名
    slug_field = 'category'
    # urls.pyでのキーワードの名前
    slug_url_kwarg = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        # 選択されたカテゴリーの質問を取得
        context['categorized_questions'] = Questions.objects.filter(category=self.object.category)
        # 質問に対する回答の数
        context['number_of_answer'] = self.object.answerforquestion_set.all().count()
        # 最新の解決済みの質問を取得  
        context['solved_questions'] = Questions.objects.filter(is_solved=True, category=self.object.category).prefetch_related(
            Prefetch('answerforquestion_set', queryset=AnswerForQuestion.objects.filter(is_best_answer=True))
        ).all()
        return context


@login_required
def decide_best_answer(request, *args, **kwargs):
    try:
        # ベストアンサーの回答を渡す
        best_answer = AnswerForQuestion.objects.get(id=kwargs['pk'])
    # 例外処理：もし、回答が存在しない場合、警告文を表示させる。
    except AnswerForQuestion.DoesNotExist:
        messages.warning(request, 'この解答はすでに削除されています')
        return HttpResponseRedirect(reverse_lazy('questions:question_detail', kwargs={'pk': best_answer.question.id}))
    # 自分の回答をベストアンサーに選ぼうとしている時、エラーを出す
    if request.user == best_answer.user:
        messages.warning(request, '自分自身の回答はベストアンサーにできません')
        return HttpResponseRedirect(reverse_lazy('questions:question_detail', kwargs={'pk': best_answer.question.id}))
    else:
        # 
        if best_answer.question.is_solved:
            messages.warning(request, 'ベストアンサーはすでに選ばれています')
            return HttpResponseRedirect(reverse_lazy('questions:question_detail', kwargs={'pk': best_answer.question.id}))
        else:
            best_answer.is_best_answer = True
            best_answer.question.is_solved = True
            best_answer.save()
            best_answer.question.save()
    return HttpResponseRedirect(reverse_lazy('questions:question_detail', kwargs={'pk': best_answer.question.id}))


class ListOfQuestionsForEachUniversity(DetailView):
    model = Schools
    template_name = 'question/list_of_questions_for_each_university.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.object
        context['solved_questions'] = Questions.objects.filter(university=school, is_solved=True).prefetch_related(
            Prefetch('answerforquestion_set', queryset=AnswerForQuestion.objects.filter(is_best_answer=True))
        )
        return context