from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('comingsoon/', views.ComingSoonView.as_view(), name='comingsoon'),
    path('regist/', views.RegistUserView.as_view(), name='regist'),
    path('user_login/', views.UserLoginView.as_view(), name='user_login'),
    path('user_logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('<slug:username>/account_setting', views.AccountSettingView.as_view(), name='account_setting'),
    path('password_change/', views.password_change, name='password_change'),
    path('user_ranking/', views.UserRankingView.as_view(), name='user_ranking'),
    path('research_university/', views.ResearchUniversity.as_view(), name='research_university'),
    path('follow_for_user/', views.follow_for_user_view, name='follow_for_user'),
    path('like_for_university/', views.like_for_university_view, name='like_for_university'),
    path('university_detail/<int:pk>', views.UniversityDetailView.as_view(), name='university_detail'),
    path('students_by_university/<int:pk>', views.StudentsByUniversityView.as_view(), name='students_by_university'),
]
