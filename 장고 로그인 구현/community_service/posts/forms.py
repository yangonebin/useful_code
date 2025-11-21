# posts/forms.py

from django import forms
from .models import Post, Comment

# F06: 게시글 작성을 위한 Django ModelForm 클래스 구현
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content'] 
        # author와 created_at은 view 함수에서 자동으로 채워줄 예정이므로 fields에서 제외

# F06: 댓글 작성을 위한 Django ModelForm 클래스 구현
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 
        # post, author, created_at은 view 함수에서 자동으로 채워줄 예정이므로 fields에서 제외