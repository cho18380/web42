from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    post_list = Post.objects.order_by('-created_at')
    context = {'post_list': post_list}
    return render(request, 'home.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author field of the post to the current user's author object
            post.created_at = timezone.now()
            post.save()
            return redirect('blog:home')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})
