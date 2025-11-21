# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm # F03에서 정의한 폼 임포트
from .models import User # F02에서 정의한 커스텀 User 모델 임포트

# F09: 사용자 등록 (Sign Up)
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index') # 로그인된 사용자는 인덱스로 리다이렉트
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원가입 성공 후 자동 로그인 (선택 사항)
            auth_login(request, user) 
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()
        
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# F07: 사용자 인증 (Log In)
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index') # 로그인된 사용자는 인덱스로 리다이렉트

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 유효성 검사 통과 시 사용자 인증 및 세션 로그인
            auth_login(request, form.get_user())
            # settings.LOGIN_REDIRECT_URL 설정에 따라 리다이렉트됨 (여기서는 '/')
            return redirect(request.GET.get('next') or 'posts:index') 
    else:
        form = AuthenticationForm()
        
    context = {
        'form': form,
    }
    # accounts/login.html 템플릿 필요
    return render(request, 'accounts/login.html', context)

# F08: 사용자 로그아웃 (Log Out)
@login_required # 로그인한 사용자만 접근 가능
def logout(request):
    auth_logout(request)
    # settings.LOGOUT_REDIRECT_URL 설정에 따라 리다이렉트됨 (여기서는 '/')
    return redirect('posts:index')

from .forms import CustomUserCreationForm, CustomUserChangeForm # 폼 임포트

# F10: 사용자 정보 수정 (Update)
@login_required
def update(request):
    if request.method == 'POST':
        # instance에 현재 로그인된 사용자 정보를 넣어 폼을 생성
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:index') # 수정 후 인덱스로 리다이렉트
    else:
        form = CustomUserChangeForm(instance=request.user)
        
    context = {
        'form': form,
    }
    # accounts/update.html 템플릿 필요
    return render(request, 'accounts/update.html', context)

# F12: 비밀번호 변경 (Change Password)
@login_required
def change_password(request):
    if request.method == 'POST':
        # request.user를 instance로 전달해야 비밀번호 해시가 올바르게 작동
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 세션 해시 업데이트: 비밀번호 변경 후에도 로그아웃되지 않도록 함
            update_session_auth_hash(request, user) 
            return redirect('posts:index') 
    else:
        form = PasswordChangeForm(request.user)
        
    context = {
        'form': form,
    }
    # accounts/change_password.html 템플릿 필요
    return render(request, 'accounts/change_password.html', context)

# F11: 사용자 계정 삭제 (Delete)
@login_required
def delete(request):
    # POST 요청으로만 처리
    if request.method == 'POST':
        request.user.delete() # 현재 로그인된 사용자(request.user) 삭제
        auth_logout(request) # 사용자 삭제 후 로그아웃 처리
        return redirect('posts:index')
    
    # POST 요청이 아닌 경우 접근을 막거나 경고 페이지를 보여줄 수 있음
    return redirect('posts:index')