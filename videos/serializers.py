from rest_framework import serializers
from .models import Video
from moviepy.editor import VideoFileClip
import tempfile, os
from analysis.utils import analyze_video

BODY_PART_MAPPING = {
    "하체": "lower_body",
    "등": "back",
    "가슴": "chest",
    "어깨": "shoulder",
    "팔": "arm",
    "코어": "core",
}

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video_file', 'uploaded_at', 'exercise_name', 'body_part']
        read_only_fields = ['uploaded_at', 'is_analyzed', 'result_json']

    # ✅ 길이 제한 검사 (20초 이하)
    def validate_video_file(self, file):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name

        try:
            clip = VideoFileClip(temp_path)
            if clip.duration > 20:
                raise serializers.ValidationError("20초 이하의 영상만 업로드할 수 있습니다.")
            clip.close()
        except Exception:
            raise serializers.ValidationError("영상 파일을 분석할 수 없습니다.")
        finally:
            os.remove(temp_path)
        return file

    def create(self, validated_data):
        user = self.context['request'].user
        exercise_name = validated_data.get("exercise_name", "헬스")
        body_part_ko = validated_data.get("body_part")

        # ✅ 한글 → 분석용 영문 키로 매핑
        body_part_en = BODY_PART_MAPPING.get(body_part_ko, "core")  # 기본값 'core'

        video = Video.objects.create(user=user, **validated_data)

        result = analyze_video(video.video_file.path, video, exercise_name, body_part_en)

        # 결과를 응답 데이터로 구성
        response_data = {
            "id": video.id,
            "exercise_name": video.exercise_name,
            "body_part": video.body_part,
            "video_url": video.video_file.url,
            "uploaded_at": video.uploaded_at,
            "analysis": result,
        }
        return response_data
