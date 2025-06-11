from django.db import models
from videos.models import Video

class AnalysisResult(models.Model):
    video = models.OneToOneField(
        Video, on_delete=models.CASCADE, related_name='analysis_result'
    )
    score = models.IntegerField()
    feedback = models.TextField()
    problem_joints = models.JSONField(blank=True, null=True)
    skeleton_image = models.ImageField(upload_to='analysis_images/', blank=True, null=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.video.video_file.name}"


class PosePoint(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='pose_points')
    frame_number = models.IntegerField()
    keypoints = models.JSONField()  # 예: [{"x": 0.52, "y": 0.71}, ...]

    def __str__(self):
        return f"Frame {self.frame_number} - {self.video.video_file.name}"
