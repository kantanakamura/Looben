from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('messaging/', views.MessageView.as_view(), name='messaging'),
    path('job/', views.JobView.as_view(), name='job'),
    path('regist/', views.RegistUserView.as_view(), name='regist'),
    path('user_login/', views.UserLoginView.as_view(), name='user_login'),
    path('user_logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('<slug:username>/account_setting', views.AccountSettingView.as_view(), name='account_setting'),
    path('password_change/', views.password_change, name='password_change'),
    path('user_ranking/', views.UserRankingView.as_view(), name='user_ranking'),
    path('research_university/', views.ResearchUniversity.as_view(), name='research_university'),
    path('<slug:username>/', views.DashboardView.as_view(), name='dashboard'),
    path('<slug:username>/connect', views.connect_view, name='connect'),
    path('<slug:username>/save', views.save_users_view, name='save_user'),
    path('save_university/<int:school_id>', views.save_university_view, name='save_university'),
    path('university_detail/<int:pk>', views.UniversityDetailView.as_view(), name='university_detail'),
    path('students_by_university/<int:pk>', views.StudentsByUniversityView.as_view(), name='students_by_university'),
]
