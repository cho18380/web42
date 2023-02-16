#import logging

from django.core.paginator import Paginator
from django.db.models import Q
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
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    post_list = Post.objects.order_by('-create_date')
    board_announce = Post.objects.filter(board_name='announce')
    board_daretalk = Post.objects.filter(board_name='daretalk')
    board_labnewsroom = Post.objects.filter(board_name='labnewsroom')
    board_projectex = Post.objects.filter(board_name='projectex')
    board_info = Post.objects.filter(board_name='info')
    board_ref = Post.objects.filter(board_name='ref')
    board_weeklynews = Post.objects.filter(board_name='weeklynews')
    board_ceotalk = Post.objects.filter(board_name='ceotalk')
    board_client = Post.objects.filter(board_name='client')
    board_forum = Post.objects.filter(board_name='forum')
    if kw:
        post_list = post_list.filter(
            Q(subject__icontains=kw) |  # 제목
            Q(content__icontains=kw) |  # 내용
            Q(comment__content__icontains=kw) |  # 답변내용
            Q(author__username__icontains=kw) |  # 질문 글쓴이
            Q(comment__author__username__icontains=kw)  # 답변 글쓴이
        ).distinct()
    paginator = Paginator(post_list, 7)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'post_list': page_obj,
        'page': page,
        'kw': kw, 
        'board_announce':board_announce,
        'board_daretalk':board_daretalk,
        'board_labnewsroom':board_labnewsroom,
        'board_projectex':board_projectex,
        'board_info':board_info,
        'board_ref':board_ref,
        'board_weeklynews':board_weeklynews,
        'board_ceotalk':board_ceotalk,
        'board_client':board_client,
        'board_forum':board_forum,
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





"""
@login_required(login_url='common:login')
def home(request):
    #logger.info("INFO 레벨로 출력")
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    post_list = Post.objects.order_by('-create_date')
    board_announce = Post.objects.filter(board_name='announce')
    board_daretalk = Post.objects.filter(board_name='daretalk')
    board_labnewsroom = Post.objects.filter(board_name='labnewsroom')
    board_projectex = Post.objects.filter(board_name='projectex')
    board_info = Post.objects.filter(board_name='info')
    board_ref = Post.objects.filter(board_name='ref')
    board_weeklynews = Post.objects.filter(board_name='weeklynews')
    board_ceotalk = Post.objects.filter(board_name='ceotalk')
    board_client = Post.objects.filter(board_name='client')
    board_forum = Post.objects.filter(board_name='forum')
    if kw:
        post_list = post_list.filter(
            Q(subject__icontains=kw) |  # 제목
            Q(content__icontains=kw) |  # 내용
            Q(comment__content__icontains=kw) |  # 답변내용
            Q(author__username__icontains=kw) |  # 질문 글쓴이
            Q(comment__author__username__icontains=kw)  # 답변 글쓴이
        ).distinct()
    paginator = Paginator(post_list, 7)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'post_list': page_obj,
        'page': page,
        'kw': kw, 
        'board_announce':board_announce,
        'board_daretalk':board_daretalk,
        'board_labnewsroom':board_labnewsroom,
        'board_projectex':board_projectex,
        'board_info':board_info,
        'board_ref':board_ref,
        'board_weeklynews':board_weeklynews,
        'board_ceotalk':board_ceotalk,
        'board_client':board_client,
        'board_forum':board_forum,
        }
    return render(request, 'home.html', context)
    """