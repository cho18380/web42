#import logging

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseNotAllowed


from .models import *
from .forms import *

#logger = logging.getLogger('')



@login_required(login_url='common:login')
def home(request):
    #logger.info("INFO 레벨로 출력")

    board_announce_list = Post.objects.filter(board_name='announce')
    board_daretalk_list = Post.objects.filter(board_name='daretalk')
    board_labnewsroom_list = Post.objects.filter(board_name='labnewsroom')
    board_projectex_list = Post.objects.filter(board_name='projectex')
    board_info_list = Post.objects.filter(board_name='info')
    board_refo_list = Post.objects.filter(board_name='refo')
    board_weeklynews_list = Post.objects.filter(board_name='weeklynews')
    board_ceotalk_list = Post.objects.filter(board_name='ceotalk')
    board_client_list = Post.objects.filter(board_name='client')
    board_forum_list = Post.objects.filter(board_name='forum')

    page_announce = request.GET.get('page_announce', '1')
    page_daretalk = request.GET.get('page_daretalk', '1')
    page_labnewsroom = request.GET.get('page_labnewsroom', '1')
    page_projectex = request.GET.get('page_projectex', '1')
    page_info = request.GET.get('page_info', '1')
    page_refo = request.GET.get('page_refo', '1')
    page_weeklynews = request.GET.get('page_weeklynews', '1')
    page_ceotalk = request.GET.get('page_ceotalk', '1')
    page_client = request.GET.get('page_client', '1')
    page_forum = request.GET.get('page_forum', '1')

    paginator_announce = Paginator(board_announce_list, 7)
    paginator_daretalk = Paginator(board_daretalk_list, 7)
    paginator_labnewsroom = Paginator(board_labnewsroom_list, 7)
    paginator_projectex = Paginator(board_projectex_list, 7)
    paginator_info = Paginator(board_info_list, 7)
    paginator_refo = Paginator(board_refo_list, 7)
    paginator_weeklynews = Paginator(board_weeklynews_list, 7)
    paginator_ceotalk = Paginator(board_ceotalk_list, 7)
    paginator_client = Paginator(board_client_list, 7)
    paginator_forum = Paginator(board_forum_list, 7)

    page_announce_obj =  paginator_announce.get_page(page_announce)
    page_daretalk_obj =  paginator_daretalk.get_page(page_daretalk)
    page_labnewsroom_obj =  paginator_labnewsroom.get_page(page_labnewsroom)
    page_projectex_obj =  paginator_projectex.get_page(page_projectex)
    page_info_obj =  paginator_info.get_page(page_info)
    page_refo_obj =  paginator_refo.get_page(page_refo)
    page_weeklynews_obj =  paginator_weeklynews.get_page(page_weeklynews)
    page_ceotalk_obj =  paginator_ceotalk.get_page(page_ceotalk)
    page_client_obj =  paginator_client.get_page(page_client)
    page_forum_obj =  paginator_forum.get_page(page_forum)

    context = {
        'board_announce_list': page_announce_obj,
        'board_daretalk_list': page_daretalk_obj,
        'board_labnewsroom_list': page_labnewsroom_obj,
        'board_projectex_list': page_projectex_obj,
        'board_info_list': page_info_obj,
        'board_refo_list': page_refo_obj,
        'board_weeklynews_list': page_weeklynews_obj,
        'board_ceotalk_list': page_ceotalk_obj,
        'board_client_list': page_client_obj,
        'board_forum_list': page_forum_obj, 
        }
    return render(request, 'home.html', context)


@login_required(login_url='common:login')
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'post_detail.html', context)


@login_required(login_url='common:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # author 속성에 로그인 계정 저장
            post.create_date = timezone.now()
            post.save()
            return redirect('board:index')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'create_post.html', context)


@login_required(login_url='common:login')
def post_modify(request, post_id):
    post = get_object_or_404(post, pk=post_id)
    if request.user != post.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', post_id=post.id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()  # 수정일시 저장
            post.save()
            return redirect('pybo:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'post_form.html', context)


@login_required(login_url='common:login')
def post_delete(request, post_id):
    post = get_object_or_404(post, pk=post_id)
    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', post_id=post.id)
    post.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def comment_create(request, post_id):
    post = get_object_or_404(post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # author 속성에 로그인 계정 저장
            comment.create_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', post_id=post.id), comment.id))
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'post': post, 'form': form}
    return render(request, 'pybo/post_detail.html', context)


@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', post_id=comment.post.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', post_id=comment.post.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('pybo:detail', post_id=comment.post.id)
