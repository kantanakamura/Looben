from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('create_blog/', views.create_blog, name='create_blog'),
]