# accounts/forms.py

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User # 커스텀 User 모델 임포트

# F03: 사용자 등록을 위한 UserCreationForm 커스터마이징 구현
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # 기본 필드에 이메일 추가 예시
        # AbstractUser를 사용하고 별도의 필드를 추가하지 않았다면 기본 UserCreationForm을 그대로 사용해도 됩니다.

# F03: 사용자 인증을 위한 AuthenticationForm 커스터마이징 구현
class CustomAuthenticationForm(AuthenticationForm):
    # 필요에 따라 사용자 정의 인증 로직이나 필드 추가 가능
    pass

from django.contrib.auth.forms import UserChangeForm

# F10을 위한 폼: UserChangeForm 커스터마이징 구현 (일반 사용자용)
class CustomUserChangeForm(UserChangeForm):
    # 비밀번호 필드는 제외하고 사용자에게 노출할 필드만 설정
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',) # 수정 가능한 필드 선택
        # fields = '__all__' 에서 password 관련 필드만 제외하거나 위처럼 명시