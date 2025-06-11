from django.db import models
from django.conf import settings

class Video(models.Model):
    BODY_PART_CHOICES = [
        ("하체", "하체"),
        ("등", "등"),
        ("가슴", "가슴"),
        ("어깨", "어깨"),
        ("팔", "팔"),
        ("코어", "코어"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='videos'
    )
    video_file = models.FileField(upload_to='analysis_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    exercise_name = models.CharField(
        max_length=50,
        help_text="운동 이름을 입력하세요 (예: 스쿼트, 푸쉬업 등)",
        default="헬스"
    )

    body_part = models.CharField(
        max_length=10,
        choices=BODY_PART_CHOICES,
        help_text="운동 부위를 선택하세요",
        default="코어"
    )
    # 비동기로 전환 시 사용예정
    # is_analyzed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} ({self.body_part})"
