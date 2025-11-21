# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

# F02: AbstractUser를 상속받는 User Model Class 구현
class User(AbstractUser):
    # AbstractUser가 제공하는 username, email, password, first_name, last_name 등을 그대로 사용
    # 필요한 경우 여기에 추가 필드를 정의할 수 있습니다.
    # 예: nickname = models.CharField(max_length=30, unique=True, null=True)
    pass