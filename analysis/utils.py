import cv2
import mediapipe as mp
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from .gpt_utils import summarize_posepoints, generate_feedback_from_keypoints
from .models import AnalysisResult, PosePoint
from videos.utils import overlay_pose_and_save
from django.core.files import File
import tempfile, os
from .pose_constants import ABSTRACT_JOINT_TRANSLATIONS


def analyze_video(video_path, video_instance, exercise_name, body_part):
    # [1] MediaPipe Pose 초기화
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False)  # 영상 스트림용

    # [2] 영상 열기 (OpenCV)
    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    saved_frame = None  # 썸네일로 저장할 첫 유효 프레임

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 영상 끝

        # BGR → RGB 변환 (MediaPipe는 RGB 입력 요구)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # [3] MediaPipe 포즈 추정
        result = pose.process(rgb_frame)

        if result.pose_landmarks:
            keypoints = []
            for lm in result.pose_landmarks.landmark:
                keypoints.append({
                    'x': round(lm.x, 5),
                    'y': round(lm.y, 5),
                })

            # [4] PosePoint 저장
            PosePoint.objects.create(
                video=video_instance,
                frame_number=frame_idx,
                keypoints=keypoints
            )

            # [5] 썸네일용 첫 유효 프레임 저장
            if saved_frame is None:
                saved_frame = frame.copy()

        frame_idx += 1

    cap.release()
    pose.close()

    # [6] 첫 프레임 이미지 저장
    if saved_frame is not None:
        img_pil = Image.fromarray(cv2.cvtColor(saved_frame, cv2.COLOR_BGR2RGB))
        buffer = BytesIO()
        img_pil.save(buffer, format='JPEG')
        image_file = ContentFile(buffer.getvalue(), name='skeleton.jpg')
    else:
        image_file = None

    # [7] 자세 요약 및 GPT 분석
    summary_text = summarize_posepoints(video_instance, exercise_name, body_part)
    gpt_result = generate_feedback_from_keypoints(summary_text, exercise_name, body_part)

    # [8] 분석 결과 저장
    AnalysisResult.objects.create(
        video=video_instance,
        score=gpt_result["score"],
        feedback=gpt_result["feedback"],
        skeleton_image=image_file
    )

    # [9] 시각화된 분석 영상 생성
    posepoints_qs = PosePoint.objects.filter(video=video_instance).order_by("frame_number")
    posepoints_dict = {pp.frame_number: pp.keypoints for pp in posepoints_qs}
    problem_joints = gpt_result.get("problem_joints", [])

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_out:
        overlay_pose_and_save(
            video_path,
            tmp_out.name,
            posepoints_dict,
            problem_joint_names=problem_joints
        )
        tmp_out_path = tmp_out.name

    with open(tmp_out_path, 'rb') as f:
        video_instance.video_file.save('annotated_video.mp4', File(f))

    os.remove(tmp_out_path)
    os.remove(video_path)

    problem_joints_kor = [
        ABSTRACT_JOINT_TRANSLATIONS.get(j, j) for j in problem_joints
    ]

    # ✅ 최종 결과 반환
    return {
        "score": gpt_result["score"],
        "feedback": gpt_result["feedback"],
        "problem_joints": problem_joints_kor
    }
