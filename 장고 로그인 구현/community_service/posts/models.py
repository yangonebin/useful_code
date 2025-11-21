# posts/models.py

from django.db import models
from django.conf import settings # AUTH_USER_MODEL을 가져오기 위함

# F04: Django Post 모델 클래스 구현 (제목, 내용, 작성자, 작성일 등)
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # 작성자는 settings.AUTH_USER_MODEL(accounts.User)과 연결
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True) # 선택적 추가 가능

    def __str__(self):
        return self.title

# F05: Django Comment 모델 클래스 구현 (게시글, 작성자, 내용, 작성일)
class Comment(models.Model):
    # 게시글 (Post)와 연결
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    # 작성자는 settings.AUTH_USER_MODEL(accounts.User)과 연결
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}'