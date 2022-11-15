from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create_review/', views.create_review_of_university, name='create_review_of_university'),
    path('review_list_of_universities/<int:pk>', views.ReviewListOfUniversities.as_view(), name='review_list_of_universities'),
]