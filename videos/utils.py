import cv2

# 관절을 연결할 인덱스 쌍 (MediaPipe 33개 기준)
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

def overlay_pose_and_save(input_path, output_path, posepoints_dict, problem_joint_names=None):
    # MediaPipe의 관절 인덱스와 명칭 매핑
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

    problem_joint_names = problem_joint_names or []

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # mp4 파일로 저장
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        keypoints = posepoints_dict.get(frame_idx)

        if keypoints:
            # 1. 관절 점 찍기 (문제 관절은 빨간 점, 나머지는 초록 점)
            for idx, pt in enumerate(keypoints):
                x = int(pt['x'] * width)
                y = int(pt['y'] * height)
                joint_name = JOINT_NAMES[idx] if idx < len(JOINT_NAMES) else None

                if joint_name in problem_joint_names:
                    color = (0, 0, 255)  # 🔴 빨간색 (문제 관절)
                else:
                    color = (0, 255, 0)  # 🟢 초록색 (정상 관절)

                cv2.circle(frame, (x, y), 5, color, -1)

            # 2. 관절 연결선 그리기 (노란색)
            for idx1, idx2 in POSE_CONNECTIONS:
                if idx1 < len(keypoints) and idx2 < len(keypoints):
                    x1 = int(keypoints[idx1]['x'] * width)
                    y1 = int(keypoints[idx1]['y'] * height)
                    x2 = int(keypoints[idx2]['x'] * width)
                    y2 = int(keypoints[idx2]['y'] * height)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)  # 노란 선

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
