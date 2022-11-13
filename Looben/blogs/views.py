from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404 


from .forms import CreateBlogForm
from .models import Blog, LikeForBlog
from accounts.models import FollowForUser
    
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
                if keyword_query in blog.content:
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