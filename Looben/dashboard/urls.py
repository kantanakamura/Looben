from django.urls import path 

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('<slug:username>/post_in_dashboard', views.PostInDashboardView.as_view(), name='post_in_dashboard'),
    path('<slug:username>/review_in_dashboard', views.ReviewInDashboardView.as_view(), name='review_in_dashboard'),
    path('<slug:username>/following_in_dashboard', views.FollowingInDashboardView.as_view(), name='following_in_dashboard'),
    path('<slug:username>/followed_in_dashboard', views.FollowedInDashboardView.as_view(), name='followed_in_dashboard'),
]