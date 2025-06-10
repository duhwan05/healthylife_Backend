from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

# 🔧 사용자 생성을 위한 커스텀 매니저 클래스
class UserManager(BaseUserManager):
    # 일반 사용자 생성 메서드
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수입니다.")  # 이메일 필수 입력 체크
        email = self.normalize_email(email)  # 이메일 형식 표준화 (@ 대소문자 처리 등)
        user = self.model(email=email, username=username, **extra_fields)  # User 인스턴스 생성
        user.set_password(password)  # 비밀번호 해싱 저장
        user.save(using=self._db)  # DB에 저장
        return user

    # 슈퍼유저 생성 메서드 (createsuperuser 명령어에서 사용됨)
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)  # 관리자 권한 부여
        extra_fields.setdefault("is_superuser", True)  # 슈퍼유저 권한 부여
        return self.create_user(email, username, password, **extra_fields)  # 일반 사용자 생성 로직 재사용

# 사용자 모델 클래스 (기본 인증 User 모델 대체)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # 로그인 ID로 사용할 이메일 (중복 불가)
    username = models.CharField(max_length=30)  # 사용자 표시 이름
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)  # 프로필 이미지 (선택)
    date_joined = models.DateTimeField(default=timezone.now)  # 가입 시간
    is_active = models.BooleanField(default=True)  # 계정 활성 상태 (False면 로그인 불가)
    is_staff = models.BooleanField(default=False)  # 관리자 사이트 접근 여부

    # 로그인 시 사용할 필드 (기본은 username이지만 여기선 email 사용)
    USERNAME_FIELD = "email"
    # createsuperuser 시 추가로 입력받을 필드
    REQUIRED_FIELDS = ["username"]

    # 사용자 생성 시 사용할 매니저 지정
    objects = UserManager()

    # 객체를 문자열로 표현할 때 email 출력
    def __str__(self):
        return self.email
