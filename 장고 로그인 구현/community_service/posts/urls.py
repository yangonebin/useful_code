# posts/urls.py

from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # F13: 게시글 목록 조회 (Index)
    path('', views.index, name='index'), 
    
    # F14: 게시글 생성 (Create)
    path('create/', views.create, name='create'),
    
    # F15: 단일 게시글 조회 (Detail)
    # <int:pk>는 URL에서 게시글의 ID(Primary Key)를 변수로 받겠다는 의미입니다.
    path('<int:post_pk>/', views.detail, name='detail'), 
    
    # F16: 게시글 수정 (Update)
    path('<int:post_pk>/update/', views.update, name='update'),
    
    # F17: 게시글 삭제 (Delete)
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    
    # F18: 댓글 생성 (Comment Create) - Detail 페이지에서 처리될 예정
    path('<int:post_pk>/comments/', views.comment_create, name='comment_create'),
    
    # F19: 댓글 삭제 (Comment Delete)
    # 게시글 ID와 댓글 ID를 모두 받아서 특정 댓글을 삭제합니다.
    path('<int:post_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]