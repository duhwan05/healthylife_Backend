from rest_framework import serializers
from .models import Video
from moviepy.editor import VideoFileClip
import tempfile, os
from analysis.utils import analyze_video

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video_file', 'uploaded_at', 'exercise_name', 'is_analyzed', 'result_json']
        read_only_fields = ['uploaded_at', 'is_analyzed', 'result_json']

    # ✅ 길이 제한 검사 (10초 이하)
    def validate_video_file(self, file):
        # 파일 확장자 체크도 필요하면 여기에 추가 가능
        # 임시 파일 저장
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
            os.remove(temp_path)  # 임시 파일 삭제
        return file

    def create(self, validated_data):
        user = self.context['request'].user
        exercise_name = validated_data.get("exercise_name", "헬스")
        video = Video.objects.create(user=user, **validated_data)

        # 분석 실행 + 결과 반환 받기
        result = analyze_video(video.video_file.path, video, exercise_name)

        # 결과를 serializer.data + 분석 결과로 구성해 반환
        response_data = {
            "id": video.id,
            "exercise_name": video.exercise_name,
            "video_url": result["video_url"],
            "score": result["score"],
            "feedback": result["feedback"],
            "uploaded_at": video.uploaded_at,
        }
        return response_data