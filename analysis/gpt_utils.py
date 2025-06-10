import json
from openai import OpenAI
from django.conf import settings
from .models import PosePoint

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# 지피티 기반 피드백 생성
def generate_feedback_from_keypoints(summary_text: str, exercise_name: str) -> dict:
    prompt = f"""
    사용자가 '{exercise_name}' 운동을 수행하고 있습니다.
    아래는 사용자의 운동 자세 요약 정보입니다:

    {summary_text}

    이 정보를 바탕으로 다음 항목을 생성하세요:

    1. 친절하고 간결한 피드백 문장 (1~2문장)으로 보여주고 문제점이 어느 부위인지 말해주기
    2. 전반적인 자세 점수를 0~100점 사이의 정수로 매기기
    3. 문제가 있는 관절 이름을 리스트로 반환 (MediaPipe 기준으로 예: "left_knee", "right_shoulder" 등)

    결과는 반드시 JSON 형식만 출력하세요. 다음 규칙을 지키세요:
    - 모든 키와 문자열은 " (double quotes) 로 감싸야 합니다
    - JSON 외의 텍스트는 포함하지 마세요

    {{
        "score": 점수,
        "feedback": "운동 자세에 대한 피드백 문장",
        "problem_joints": ["관절이름1", "관절이름2", ...],
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

# 자세요약 해서 지피티에게 넘기는 역할
def summarize_posepoints(video_instance):
    posepoints = PosePoint.objects.filter(video=video_instance).order_by("frame_number")
    summary_lines = []

    for pp in posepoints[::10]:  # 🔁 10프레임 간격 샘플링
        keypoints = pp.keypoints
        try:
            left_shoulder = keypoints[11]
            right_shoulder = keypoints[12]
            left_knee = keypoints[25]
            right_knee = keypoints[26]

            shoulder_diff = abs(left_shoulder['y'] - right_shoulder['y'])
            knee_diff = abs(left_knee['y'] - right_knee['y'])

            summary_lines.append(
                f"{pp.frame_number}프레임: 어깨 수평 차이={shoulder_diff:.3f}, 무릎 높이 차이={knee_diff:.3f}"
            )

        except (IndexError, KeyError):
            continue  # 좌표 누락 프레임은 생략

    return "\n".join(summary_lines)
