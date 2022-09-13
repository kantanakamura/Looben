from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import CreateBlogForm
    
    
def create_blog(request):
    create_blog_form = CreateBlogForm(request.POST or None)
    if create_blog_form.is_valid():
        create_blog_form.instance.user = request.user
        create_blog_form.save()
        return redirect('accounts:research_university')
    return render(
        request, 'blog/create_blog.html', context={
            'create_blog_form': create_blog_form
        }
    )