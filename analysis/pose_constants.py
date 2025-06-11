# 관절 이름 리스트 (MediaPipe 33개 기준)
JOINT_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer",
    "right_eye_inner", "right_eye", "right_eye_outer",
    "left_ear", "right_ear",
    "mouth_left", "mouth_right",
    "left_shoulder", "right_shoulder",
    "left_elbow", "right_elbow",
    "left_wrist", "right_wrist",
    "left_pinky", "right_pinky", "left_index", "right_index",
    "left_thumb", "right_thumb",
    "left_hip", "right_hip",
    "left_knee", "right_knee",
    "left_ankle", "right_ankle",
    "left_heel", "right_heel",
    "left_foot_index", "right_foot_index"
]

# 관절 연결 (MediaPipe 33개 기준)
POSE_CONNECTIONS = [
    (11, 13), (13, 15),    # 왼쪽 팔
    (12, 14), (14, 16),    # 오른쪽 팔
    (11, 12),              # 어깨 연결
    (23, 24),              # 엉덩이 연결
    (11, 23), (12, 24),    # 몸통 연결
    (23, 25), (25, 27),    # 왼쪽 다리
    (24, 26), (26, 28),    # 오른쪽 다리
    (27, 29), (28, 30),    # 무릎 아래
    (29, 31), (30, 32)     # 발끝
]

# 추상 관절 → 실제 관절 이름 매핑
ABSTRACT_JOINT_MAP = {
    # 상체
    "head": [
        "nose", "left_eye_inner", "left_eye", "left_eye_outer",
        "right_eye_inner", "right_eye", "right_eye_outer",
        "left_ear", "right_ear", "mouth_left", "mouth_right"
    ],
    "neck": ["left_shoulder", "right_shoulder"],  # 어깨 근처를 목 기준으로 추정
    "scapula": ["left_shoulder", "right_shoulder"],  # 견갑골 = 어깨
    "shoulders": ["left_shoulder", "right_shoulder"],
    "spine": ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
    "torso": ["left_shoulder", "right_shoulder", "left_hip", "right_hip"],
    "core": ["left_shoulder", "right_shoulder", "left_hip", "right_hip", "left_knee", "right_knee"],  # 코어 강화 관점
    "pelvis": ["left_hip", "right_hip"],
    "hip": ["left_hip", "right_hip"],

    # 팔
    "left_arm": ["left_shoulder", "left_elbow", "left_wrist"],
    "right_arm": ["right_shoulder", "right_elbow", "right_wrist"],
    "arms": ["left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist"],

    # 손
    "left_hand": ["left_wrist", "left_thumb", "left_index", "left_pinky"],
    "right_hand": ["right_wrist", "right_thumb", "right_index", "right_pinky"],
    "hands": [
        "left_wrist", "right_wrist",
        "left_thumb", "right_thumb",
        "left_index", "right_index",
        "left_pinky", "right_pinky"
    ],

    # 다리
    "left_leg": ["left_hip", "left_knee", "left_ankle"],
    "right_leg": ["right_hip", "right_knee", "right_ankle"],
    "legs": [
        "left_hip", "right_hip",
        "left_knee", "right_knee",
        "left_ankle", "right_ankle"
    ],

    # 발
    "left_foot": ["left_heel", "left_foot_index"],
    "right_foot": ["right_heel", "right_foot_index"],
    "feet": [
        "left_ankle", "right_ankle",
        "left_heel", "right_heel",
        "left_foot_index", "right_foot_index"
    ],
}

# 추상 관절 → 한글 매핑
ABSTRACT_JOINT_TRANSLATIONS = {
    # 구체 관절 (기존)
    "nose": "코",
    "left_eye_inner": "왼쪽 눈 안쪽",
    "left_eye": "왼쪽 눈",
    "left_eye_outer": "왼쪽 눈 바깥쪽",
    "right_eye_inner": "오른쪽 눈 안쪽",
    "right_eye": "오른쪽 눈",
    "right_eye_outer": "오른쪽 눈 바깥쪽",
    "left_ear": "왼쪽 귀",
    "right_ear": "오른쪽 귀",
    "mouth_left": "입 왼쪽",
    "mouth_right": "입 오른쪽",
    "left_shoulder": "왼쪽 어깨",
    "right_shoulder": "오른쪽 어깨",
    "left_elbow": "왼쪽 팔꿈치",
    "right_elbow": "오른쪽 팔꿈치",
    "left_wrist": "왼쪽 손목",
    "right_wrist": "오른쪽 손목",
    "left_pinky": "왼쪽 새끼손가락",
    "right_pinky": "오른쪽 새끼손가락",
    "left_index": "왼쪽 검지",
    "right_index": "오른쪽 검지",
    "left_thumb": "왼쪽 엄지손가락",
    "right_thumb": "오른쪽 엄지손가락",
    "left_hip": "왼쪽 엉덩이",
    "right_hip": "오른쪽 엉덩이",
    "left_knee": "왼쪽 무릎",
    "right_knee": "오른쪽 무릎",
    "left_ankle": "왼쪽 발목",
    "right_ankle": "오른쪽 발목",
    "left_heel": "왼쪽 뒤꿈치",
    "right_heel": "오른쪽 뒤꿈치",
    "left_foot_index": "왼쪽 발끝",
    "right_foot_index": "오른쪽 발끝",

    # 추상 관절 (추가)
    "head": "머리",
    "neck": "목",
    "scapula": "견갑골",  # 어깨
    "shoulders": "어깨",
    "spine": "척추",
    "torso": "몸통",
    "core": "코어",
    "pelvis": "엉덩이",
    "hip": "엉덩이",
    "left_arm": "왼팔",
    "right_arm": "오른팔",
    "arms": "팔",
    "left_hand": "왼손",
    "right_hand": "오른손",
    "hands": "손",
    "left_leg": "왼다리",
    "right_leg": "오른다리",
    "legs": "다리",
    "left_foot": "왼발",
    "right_foot": "오른발",
    "feet": "발",
}