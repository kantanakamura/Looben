from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404 
from django.db.models import Q

from .forms import CreateBlogForm, EditBlogPostForm
from .models import Blog, LikeForBlog
from accounts.models import FollowForUser, Users


@login_required
def create_blog(request):
    create_blog_form = CreateBlogForm(request.POST or None, files=request.FILES)
    if create_blog_form.is_valid():
        create_blog_form.instance.author = request.user
        create_blog_form.save()
        return redirect('blogs:blog_list')
    return render(
        request, 'blog/create_blog.html', context={
            'create_blog_form': create_blog_form
        }
    )
    
class CheckForUserMatchMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        target_blog_post = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return self.request.user == target_blog_post.author
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Only user who made this author have access to this view'}
        )
    

class EditBlogPostView(CheckForUserMatchMixin, UpdateView):
    template_name = 'blog/edit_blog_post.html'
    form_class = EditBlogPostForm
    model = Blog
    
    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.id}) 
    
    
class BlogListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        number_of_following_user = FollowForUser.objects.filter(user=user).count()
        number_of_followed_user = FollowForUser.objects.filter(followed_user=user).count()
        number_of_blog_post = Blog.objects.filter(author=user).count()
        newest_blog_posts = Blog.objects.order_by('-created_at')[:6]
        most_viewed_posts = Blog.objects.order_by('-total_number_of_view')[:6]
        if 'search' in self.request.GET:
            keyword_query = request.GET.get('search')
            blogs = list(Blog.objects.all())
            searched_blogs = []
            for blog in blogs:
                if keyword_query in blog.meta_description:
                    searched_blogs.append(blog)
            number_of_searched_blogs = len(searched_blogs)
            user_searched_something = True
        else:
            searched_blogs = []
            number_of_searched_blogs = 0
            user_searched_something = False
        return render(request, 'blog/blog_list.html', {
            'number_of_following_user': number_of_following_user,
            'number_of_followed_user': number_of_followed_user,
            'number_of_blog_post': number_of_blog_post,
            'newest_blog_posts': newest_blog_posts,
            'most_viewed_posts': most_viewed_posts,
            'number_of_searched_blogs': number_of_searched_blogs,
            'user_searched_something': user_searched_something,
            'searched_blogs': searched_blogs,
            })
        
        
class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'
    model = Blog
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.author
        self.object.total_number_of_view += 1
        self.object.save()
        context['number_of_following_user'] = FollowForUser.objects.filter(user=user).count()
        context['number_of_followed_user'] = FollowForUser.objects.filter(followed_user=user).count()
        context['number_of_blog_post'] = Blog.objects.filter(author=user).count()
        context['number_of_like_for_blog_post'] = self.object.likeforblog_set.count()
        context['related_blog_posts'] = Blog.objects.filter(~Q(id=self.object.id), tag=self.object.tag).order_by('-total_number_of_view')[:4]
        context['newest_blog_posts'] = Blog.objects.filter(~Q(id=self.object.id)).order_by('-created_at')[:4]
        if self.object.likeforblog_set.filter(user=self.request.user).exists():
                context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False
        return context
    
@login_required
def like_for_post(request):
    post_pk = request.POST.get('post_pk')
    context = {
        'user': f'{request.user.username}',
    }
    post = get_object_or_404(Blog, pk=post_pk)
    like = LikeForBlog.objects.filter(target=post, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=post, user=request.user)
        context['method'] = 'create'
    context['like_for_post_count'] = post.likeforblog_set.count()
    return JsonResponse(context)


class LikedBlogListView(LoginRequiredMixin, ListView):
    template_name = 'blog/liked_blog_list.html'
    model = LikeForBlog
    ordering = ['-timestamp']
    
    def get_queryset(self, **kwargs):
        query = super().get_queryset(**kwargs)
        request_user = get_object_or_404(Users, id=self.request.user.id)
        query = query.filter(user=request_user)
        return query
    
    
class InOrderBlogListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        blog_posts_order_by_date = Blog.objects.order_by('-created_at')[:20]
        blog_posts_order_by_number_of_view = Blog.objects.order_by('-total_number_of_view')[:20]
        official_blog_post_lists = Blog.objects.filter(is_official=True)[:20]
        return render(request, 'blog/in_order_blog_post.html', {
            'blog_posts_order_by_date': blog_posts_order_by_date,
            'blog_posts_order_by_number_of_view': blog_posts_order_by_number_of_view,
            'official_blog_post_lists': official_blog_post_lists
            })
    