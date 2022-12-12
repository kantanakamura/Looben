from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('create_blog/', views.create_blog, name='create_blog'),
    path('blog_list/', views.BlogListView.as_view(), name='blog_list'),
    path('in_order_blog_list/', views.InOrderBlogListView.as_view(), name='in_order_blog_list'), 
    path('edit_post/<int:pk>', views.EditBlogPostView.as_view(), name='edit_post'), 
    path('delete_post/<int:pk>', views.DeletePostView.as_view(), name='delete_post'), 
]