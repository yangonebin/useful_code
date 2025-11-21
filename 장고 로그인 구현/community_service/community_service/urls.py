# community_service/urls.py (프로젝트 Root)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # URL 경로가 'accounts/'로 시작하면 accounts.urls로 라우팅
    path('accounts/', include('accounts.urls')), 
    
    # URL 경로가 'posts/'로 시작하면 posts.urls로 라우팅 (선택 사항)
    # posts 앱의 URL 구조에 따라 이 부분을 생략하고 메인 경로만 남길 수 있습니다.
    # path('posts/', include('posts.urls')),       
    
    # F13에 따라 posts.index를 홈('/')으로 지정
    path('', include('posts.urls')), 
]