import json
from openai import OpenAI
from django.conf import settings
from .models import PosePoint

client = OpenAI(api_key=settings.OPENAI_API_KEY)

PART_INSTRUCTION = {
    "lower_body": "무릎, 엉덩이, 발목의 정렬과 대칭성을 기준으로 평가하세요.",
    "back": "척추의 곡선 유지, 견갑골의 움직임, 몸통의 안정성을 기준으로 평가하세요.",
    "chest": "가슴이 들려 있는지, 어깨의 위치와 팔의 움직임을 기준으로 평가하세요.",
    "shoulder": "어깨의 수평 정렬과 어깨 관절의 안정성을 기준으로 평가하세요.",
    "arm": "팔꿈치와 손목의 정렬, 팔의 움직임 범위를 기준으로 평가하세요.",
    "core": "어깨-골반-발목의 수직 정렬과 복부 및 허리의 안정성을 기준으로 평가하세요.",
}


# 🧠 GPT 피드백 생성
def generate_feedback_from_keypoints(summary_text: str, exercise_name: str, body_part: str) -> dict:
    part_instruction = PART_INSTRUCTION[body_part]

    prompt = f"""
    당신은 피트니스 자세 평가 전문가입니다.

    다음은 사용자 운동 영상의 요약 정보입니다:

    - 운동 이름: {exercise_name}
    - 분석 부위: {body_part}
    - 자세 요약:
    {summary_text}

    부위별 평가 기준:
    {part_instruction}

    이 정보를 바탕으로 다음 JSON 형식으로 분석 결과를 생성하세요:

    1. "feedback": 문제점을 설명하고, 어떤 관절/부위에 개선이 필요한지 알려주는 간단하고 친절한 문장 (2문장 이하)
    2. "score": 전체 자세에 대해 0~100 사이의 정수 점수 표출, 문제 프레임 있을때마다 5점씩 차감
    3. "problem_joints": 문제가 있는 관절 이름을 리스트로 (MediaPipe 명칭 기준: "left_knee", "right_shoulder" 등)

    🚫 JSON 외의 텍스트는 포함하지 마세요.

    형식:
    {{
        "score": 85,
        "feedback": "어깨 높이가 다르고 무릎의 대칭이 부족해요. 어깨와 무릎 위치를 신경써보세요.",
        "problem_joints": ["left_shoulder", "right_knee"]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 피트니스 자세 평가 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        content = response.choices[0].message.content
        result = json.loads(content)

        return {
            "score": int(result["score"]),
            "feedback": result["feedback"],
            "problem_joints": result.get("problem_joints", [])
        }

    except Exception as e:
        return {
            "score": 0,
            "feedback": f"분석 중 오류가 발생했습니다. ({str(e)})"
        }


# 📊 포즈 요약 (운동 부위에 따라 다른 관절 사용)
def summarize_posepoints(video_instance, exercise_name: str, body_part: str):
    posepoints = PosePoint.objects.filter(video=video_instance).order_by("frame_number")
    summary_lines = []

    for pp in posepoints[::10]:  # 🔁 10프레임 간격 샘플링
        keypoints = pp.keypoints
        try:
            if body_part == "lower_body":
                left_knee = keypoints[25]
                right_knee = keypoints[26]
                knee_diff = abs(left_knee['y'] - right_knee['y'])
                summary_lines.append(f"{pp.frame_number}프레임: 무릎 높이 차이={knee_diff:.3f}")

            elif body_part == "back":
                left_shoulder = keypoints[11]
                right_shoulder = keypoints[12]
                shoulder_diff = abs(left_shoulder['z'] - right_shoulder['z'])
                summary_lines.append(f"{pp.frame_number}프레임: 어깨 전후 위치 차이(z축)={shoulder_diff:.3f}")

            elif body_part == "chest":
                left_elbow = keypoints[13]
                right_elbow = keypoints[14]
                elbow_diff = abs(left_elbow['y'] - right_elbow['y'])
                summary_lines.append(f"{pp.frame_number}프레임: 팔꿈치 높이 차이={elbow_diff:.3f}")

            elif body_part == "shoulder":
                left_shoulder = keypoints[11]
                right_shoulder = keypoints[12]
                shoulder_diff = abs(left_shoulder['y'] - right_shoulder['y'])
                summary_lines.append(f"{pp.frame_number}프레임: 어깨 높이 차이={shoulder_diff:.3f}")

            elif body_part == "arm":
                left_wrist = keypoints[15]
                right_wrist = keypoints[16]
                wrist_diff = abs(left_wrist['y'] - right_wrist['y'])
                summary_lines.append(f"{pp.frame_number}프레임: 손목 높이 차이={wrist_diff:.3f}")

            elif body_part == "core":
                shoulder = keypoints[11]
                hip = keypoints[23]
                ankle = keypoints[27]
                vertical_alignment = abs((shoulder['x'] - hip['x']) + (hip['x'] - ankle['x']))
                summary_lines.append(f"{pp.frame_number}프레임: 코어 수직 정렬 차이={vertical_alignment:.3f}")

        except (IndexError, KeyError):
            continue  # 좌표 누락 프레임은 생략

    return "\n".join(summary_lines)
