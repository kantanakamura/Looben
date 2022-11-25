from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Prefetch
from django.db.models import Q

from .forms import AnswerForQuestionForm, CommentToAnswerForm, QuestionForm
from .models import AnswerForQuestion, Questions

from accounts.models import Users, Schools
from accounts import contribution_calculation


class QuestionView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        question_seeking_answers = Questions.objects.filter(is_solved=False).all()[:4]  
        solved_questions = Questions.objects.filter(is_solved=True).order_by('-created_at').prefetch_related(
            Prefetch('answerforquestion_set', queryset=AnswerForQuestion.objects.filter(is_best_answer=True))
        )[:4]
        reliable_answerers = Users.objects.order_by('-contributed_points').all()[:3] 
        if 'search' in self.request.GET:
            keyword_query = request.GET.get('search')
            if keyword_query == '':
                searched_questions = []
                number_of_searched_questions = 0
                user_searched_anything = False
            else:
                questions = list(Questions.objects.all())
                searched_questions = []
                for question in questions:
                    if keyword_query in question.content:
                        searched_questions.append(question)
                number_of_searched_questions = len(searched_questions)
                user_searched_anything = True
        else:
            searched_questions = []
            number_of_searched_questions = 0
            user_searched_anything = False
        return render(request, 'question/question.html', {
            'question_seeking_answers': question_seeking_answers,
            'solved_questions': solved_questions,
            'reliable_answerers': reliable_answerers,
            'searched_questions': searched_questions,
            'user_searched_anything': user_searched_anything,
            'number_of_searched_questions': number_of_searched_questions,
            'searched_questions': searched_questions,
            })
    
    
@login_required
def ask_question(request):
    ask_question_form = QuestionForm(request.POST or None)
    if ask_question_form.is_valid():
        ask_question_form.instance.user = request.user
        if ask_question_form['is_anonymous'] == 'on':
            ask_question_form.instance.is_anonymous = True
        ask_question_form.save()
        contribution_calculation.for_creating_question(user=request.user)
        return redirect('questions:question')
    return render(
        request, 'question/ask_question.html', context={
            'ask_question_form': ask_question_form
        }
    )
    
    
class QuestionDetailView(DetailView):
    template_name = 'question/question_detail.html'
    model = Questions
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_of_answer'] = self.object.answerforquestion_set.all().count()
        if self.object.is_solved:           
            best_answer = self.object.answerforquestion_set.filter(is_best_answer=True).first()
            context['best_answer'] = best_answer
            context['comment_to_best_answer'] = best_answer.commenttobestanswer_set.first()
        context['newest_solved_questions'] = Questions.objects.filter(~Q(id=self.object.id), category=self.object.category, is_solved=True).order_by('created_at')[:5]
        context['answer_form'] = AnswerForQuestionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        answer_form = AnswerForQuestionForm(request.POST or None)
        if answer_form.is_valid():
            answer_form.instance.question = self.object
            answer_form.instance.user = request.user
            answer_form.save()
            return redirect('questions:question_detail', pk=self.object.id)
        else:
            context = self.get_context_data()
            context['answer_form'] = answer_form 
            return render(request, 'questions:question_detail', context)
        
    
    
class CategorizedQuestionsView(ListView):
    model = Questions
    template_name = 'question/categorized_questions.html'
    slug_field = 'category'
    slug_url_kwarg = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unsolved_questions'] = Questions.objects.filter(is_solved=False, category=self.kwargs.get('category')).all()
        context['solved_questions'] = Questions.objects.filter(is_solved=True, category=self.kwargs.get('category')).prefetch_related(
            Prefetch('answerforquestion_set', queryset=AnswerForQuestion.objects.filter(is_best_answer=True))
        ).all()
        context['category'] = self.kwargs.get('category')
        return context


class ListOfQuestionsForEachUniversity(DetailView):
    model = Schools
    template_name = 'question/list_of_questions_for_each_university.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solved_questions'] = Questions.objects.filter(university=self.object, is_solved=True).prefetch_related(
            Prefetch('answerforquestion_set', queryset=AnswerForQuestion.objects.filter(is_best_answer=True))
        )
        return context
        
        
class DecideAndCommentToBestAnswer(DetailView):
    model = AnswerForQuestion
    template_name = 'question/comment_to_best_answer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_to_answer_form'] = CommentToAnswerForm()
        context['question'] = Questions.objects.get(id=self.object.question.id)
        return context
    
    def post(self, request, *args, **kwargs):
        best_answer = self.get_object()
        comment_to_answer_form = CommentToAnswerForm(request.POST or None)
        if comment_to_answer_form.is_valid():
            if best_answer.question.is_solved:
                messages.warning(request, 'ベストアンサーはすでに選ばれています')
                return HttpResponseRedirect(reverse_lazy('questions:question_detail', kwargs={'pk': best_answer.question.id}))
            else:
                best_answer.is_best_answer = True
                best_answer.save()
                best_answer.question.is_solved = True
                best_answer.question.save()
                contribution_calculation.for_getting_best_answer(user=request.user)
                comment_to_answer_form.instance.answer = best_answer
                comment_to_answer_form.instance.commenter = request.user
                comment_to_answer_form.save()
            return redirect('questions:question_detail', pk=best_answer.question.id)
        else:
            context = self.get_context_data()
            context['comment_to_answer_form'] = comment_to_answer_form  
            return render(request, 'questions:question_detail', context)
    