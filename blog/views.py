from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login



def home(request):
    post_list = Post.objects.order_by('-created_at')
    context = {'post_list': post_list}
    return render(request, 'home.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'post_detail.html', context)

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.html')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') # Replace with your desired URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
