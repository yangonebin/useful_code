# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # F09: 회원가입 (Sign Up)
    path('signup/', views.signup, name='signup'),
    
    # F07: 로그인 (Log In)
    path('login/', views.login, name='login'),
    
    # F08: 로그아웃 (Log Out)
    path('logout/', views.logout, name='logout'),
    
    # F10: 회원정보 수정 (Update Profile)
    path('update/', views.update, name='update'),
    
    # F12: 비밀번호 변경 (Change Password)
    path('password/', views.change_password, name='change_password'),
    
    # F11: 회원 탈퇴 (Delete Account)
    path('delete/', views.delete, name='delete'),
]