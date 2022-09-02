from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('review/<int:school_id>', views.ReviewOfUniversityView.as_view(), name='review_of_university'),
]