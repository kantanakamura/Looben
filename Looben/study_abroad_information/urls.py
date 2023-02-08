from django.urls import path
from . import views

app_name = 'study_abroad_information'

urlpatterns = [
    path('create_information_post/', views.create_information_post, name='create_information_post'),
    path('information_post_list/', views.InformationPostListView.as_view(), name='information_post_list'),
    path('in_order_information_post_list/', views.InOrderInformationPostListView.as_view(), name='in_order_information_post_list'), 
    path('edit_information_post/<int:pk>', views.EditInformationPostView.as_view(), name='edit_information_post'), 
    path('delete_information_post/<int:pk>', views.DeleteInformationPostView.as_view(), name='delete_information_post'), 
]