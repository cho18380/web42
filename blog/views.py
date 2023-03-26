from django.shortcuts import render, get_object_or_404
from .models import *


def home(request):
    post_list = Post.objects.order_by('-created_at')
    context = {'post_list': post_list}
    return render(request, 'home.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'post_detail.html', context)