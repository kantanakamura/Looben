from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('question/', views.QuestionView.as_view(), name='question'),
    path('ask_question/', views.ask_question, name='ask_question'),
    path('<slug:category>/categorized_questions', views.CategorizedQuestionsView.as_view(), name='categorized_questions'),
    path('list_of_questions_for_each_university/<int:pk>', views.ListOfQuestionsForEachUniversity.as_view(), name='list_of_questions_for_each_university'),
    path('question_detail/<int:pk>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('decide_best_answer/<int:pk>', views.decide_best_answer, name='decide_best_answer'),
]