from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('create_blog/', views.create_blog, name='create_blog'),
    path('blog_list/', views.BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('like_for_post/', views.like_for_post, name='like_for_post'), 
    path('liked_blog_list/', views.LikedBlogListView.as_view(), name='liked_blog_list'), 
    path('in_order_blog_list/', views.InOrderBlogListView.as_view(), name='in_order_blog_list'), 
    path('edit_blog_post/<int:pk>', views.EditBlogPostView.as_view(), name='edit_blog_post'), 
]