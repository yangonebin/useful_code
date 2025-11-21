# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .models import Post, Comment
from .forms import PostForm, CommentForm

# F13: 전체 게시글 목록 조회 및 출력
def index(request):
    # 모든 Post 객체를 생성일(created_at) 역순으로 가져옵니다.
    posts = Post.objects.order_by('-created_at')
    
    context = {
        'posts': posts,
    }
    # posts/index.html 템플릿 필요
    return render(request, 'posts/index.html', context)

# F14: 게시글 입력 UI 제공 및 저장
@login_required 
@require_http_methods(['GET', 'POST']) # GET 또는 POST만 허용 (NF03)
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # 작성자(author)는 현재 로그인된 사용자(request.user)로 자동 설정
            post.author = request.user 
            post.save()
            # 저장 후 상세 페이지로 리다이렉트
            return redirect('posts:detail', post_pk=post.pk) 
    else: # GET 요청
        form = PostForm()
        
    context = {
        'form': form,
    }
    # posts/create.html 템플릿 필요
    return render(request, 'posts/create.html', context)

# F15: 단일 게시글 조회 및 댓글 출력
def detail(request, post_pk):
    # post_pk를 이용하여 Post 객체를 가져오거나 404 에러 발생
    post = get_object_or_404(Post, pk=post_pk)
    
    # 댓글 관련 기능 (F18에 대비)
    comment_form = CommentForm()
    
    # 해당 게시글에 연결된 모든 댓글을 가져옵니다. (related_name='comments' 사용)
    comments = post.comments.all() 
    
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
    }
    # posts/detail.html 템플릿 필요
    return render(request, 'posts/detail.html', context)

# F16: 게시글 수정 UI 제공 및 저장
@login_required 
@require_http_methods(['GET', 'POST']) # GET 또는 POST만 허용 (NF03)
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    # 작성자 본인만 수정 가능하도록 제한
    if post.author != request.user:
        return redirect('posts:detail', post_pk=post_pk)

    if request.method == 'POST':
        # instance에 기존 객체를 넣어 폼을 생성해야 수정이 됩니다.
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post_pk=post.pk) 
    else: # GET 요청 (수정 폼 보여주기)
        form = PostForm(instance=post)
        
    context = {
        'post': post,
        'form': form,
    }
    # posts/update.html 템플릿 필요
    return render(request, 'posts/update.html', context)

# F17: 단일 게시글 삭제
@login_required
@require_POST # POST 요청만 허용 (NF03)
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    # 작성자 본인만 삭제 가능하도록 제한
    if post.author == request.user:
        post.delete()
        # 삭제 후 목록 페이지로 리다이렉트
        return redirect('posts:index')
    
    # 작성자가 아닌 경우, 상세 페이지로 리다이렉트
    return redirect('posts:detail', post_pk=post_pk)

# F18: 댓글 데이터 입력 받아 저장 (Comment Create)
@require_POST # POST 요청만 허용 (NF03)
@login_required # 로그인한 사용자만 댓글 작성 가능
def comment_create(request, post_pk):
    # 1. 댓글을 달 게시글(Post)을 가져옵니다.
    post = get_object_or_404(Post, pk=post_pk)
    
    # 2. 전송된 데이터로 CommentForm을 생성합니다.
    comment_form = CommentForm(request.POST)
    
    if comment_form.is_valid():
        # 3. 폼 데이터를 바로 저장하지 않고 인스턴스만 가져옵니다.
        comment = comment_form.save(commit=False)
        
        # 4. FK 필드인 post와 author를 수동으로 지정합니다.
        comment.post = post
        comment.author = request.user
        
        # 5. DB에 최종 저장합니다.
        comment.save()
        
    # 유효성 검사 성공/실패와 관계없이 게시글 상세 페이지로 리다이렉트
    # 실패 시 detail 템플릿에서 오류 메시지를 처리해야 합니다. (템플릿 미구현 시)
    return redirect('posts:detail', post_pk=post_pk)

# posts/views.py (추가)

# F19: 댓글 삭제
@require_POST # POST 요청만 허용 (NF03)
@login_required # 로그인한 사용자만 댓글 삭제 가능
def comment_delete(request, post_pk, comment_pk):
    # 1. 삭제할 댓글 객체를 가져옵니다. (없으면 404)
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 2. 작성자 본인인지 확인합니다.
    if comment.author == request.user:
        comment.delete()
        
    # 3. 삭제 후 게시글 상세 페이지로 리다이렉트합니다.
    return redirect('posts:detail', post_pk=post_pk)