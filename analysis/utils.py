import cv2
import mediapipe as mp
import os
import tempfile
from uuid import uuid4
from io import BytesIO
from PIL import Image

from django.core.files.base import ContentFile

from .gpt_utils import summarize_posepoints, generate_feedback_from_keypoints
from .models import AnalysisResult, PosePoint
from .pose_constants import ABSTRACT_JOINT_TRANSLATIONS
from videos.utils import overlay_pose_and_save
from videos.s3_upload import upload_file_to_s3


def analyze_video(video_path, video_instance, exercise_name, body_part):
    # 1. MediaPipe Pose 인식기 초기화
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False)

    # 2. OpenCV로 비디오 열기
    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    saved_frame = None  # 첫 프레임 저장용

    # 3. 비디오를 프레임 단위로 순회
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 끝까지 읽었으면 종료

        # 4. 색상 변환 및 자세 추론
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb_frame)

        # 5. 추론 결과가 있다면 키포인트 저장
        if result.pose_landmarks:
            keypoints = [
                {'x': round(lm.x, 5), 'y': round(lm.y, 5)}
                for lm in result.pose_landmarks.landmark
            ]

            PosePoint.objects.create(
                video=video_instance,
                frame_number=frame_idx,
                keypoints=keypoints
            )

            if saved_frame is None:
                saved_frame = frame.copy()  # 첫 프레임 저장

        frame_idx += 1

    # 6. 리소스 정리
    cap.release()
    pose.close()

    # 7. 첫 프레임 이미지 -> PIL 이미지로 변환하여 ContentFile 생성
    if saved_frame is not None:
        img_pil = Image.fromarray(cv2.cvtColor(saved_frame, cv2.COLOR_BGR2RGB))
        buffer = BytesIO()
        img_pil.save(buffer, format='JPEG')
        image_file = ContentFile(buffer.getvalue(), name='skeleton.jpg')
    else:
        image_file = None

    # 8. 포즈 요약 → GPT에게 분석 요청
    summary_text = summarize_posepoints(video_instance, exercise_name, body_part)
    gpt_result = generate_feedback_from_keypoints(summary_text, exercise_name, body_part)

    # 9. 분석 결과 저장 (skeleton_image 제외)
    analysis_result = AnalysisResult.objects.create(
        video=video_instance,
        score=gpt_result["score"],
        feedback=gpt_result["feedback"],
    )

    # 10. skeleton 이미지 파일을 임시 파일로 저장 후 S3에 업로드
    skeleton_img_url = None
    if saved_frame is not None:
        tmp_img_path = os.path.join(tempfile.gettempdir(), f"skeleton_{uuid4().hex}.jpg")
        img_pil.save(tmp_img_path)

        skeleton_img_url = upload_file_to_s3(tmp_img_path, folder='analysis_image')
        os.remove(tmp_img_path)  # 로컬 파일 삭제

    # 11. 자세 키포인트 불러오기
    posepoints_qs = PosePoint.objects.filter(video=video_instance).order_by("frame_number")
    posepoints_dict = {pp.frame_number: pp.keypoints for pp in posepoints_qs}
    problem_joints = gpt_result.get("problem_joints", [])

    # 12. 분석 비디오에 키포인트 오버레이해서 영상 생성
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_out:
        overlay_pose_and_save(
            video_path,
            tmp_out.name,
            posepoints_dict,
            problem_joint_names=problem_joints
        )
        tmp_out_path = tmp_out.name
    analyzed_video_url = upload_file_to_s3(tmp_out_path, folder='analysis_videos')

    # 14. 로컬 파일 정리
    os.remove(tmp_out_path)
    os.remove(video_path)

    # 15. 문제 관절 한국어 번역
    problem_joints_kor = [
        ABSTRACT_JOINT_TRANSLATIONS.get(j, j) for j in problem_joints
    ]

    # 16. 결과 반환
    return {
        "score": gpt_result["score"],
        "feedback": gpt_result["feedback"],
        "problem_joints": problem_joints_kor,
    }
