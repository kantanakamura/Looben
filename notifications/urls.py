from django.urls import path
from . import views


app_name = 'notifications'

urlpatterns = [
    path('delete_all_notifications/', views.delete_all_notifications, name='delete_all_notifications'),
    path('notification_list/', views.NotificationList.as_view(), name='notification_list'),
]