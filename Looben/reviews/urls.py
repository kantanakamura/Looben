from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create_review/', views.CreateReviewOfUniversityView.as_view(), name='create_review_of_university'),
    path('review_in_dashboard/', views.ReviewInDashboardView.as_view(), name='review_in_dashboard'),
]