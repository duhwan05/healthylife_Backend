from django.db import models
from django.conf import settings

class Video(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='videos'
    )
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_analyzed = models.BooleanField(default=False)
    result_json = models.JSONField(blank=True, null=True)
    exercise_name = models.CharField(
    max_length=50,
    help_text="운동 이름을 입력하세요 (예: 스쿼트, 푸쉬업 등)",
    default="헬스"
    )

    def __str__(self):
        return f"{self.user.username} - {self.video_file.name}"
