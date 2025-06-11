import cv2
from analysis.pose_constants import JOINT_NAMES, POSE_CONNECTIONS, ABSTRACT_JOINT_MAP

def overlay_pose_and_save(input_path, output_path, posepoints_dict, problem_joint_names=None):
    # 문제 관절 확장
    problem_joint_names = problem_joint_names or []
    expanded_problem_joints = set()
    for name in problem_joint_names:
        if name in ABSTRACT_JOINT_MAP:
            expanded_problem_joints.update(ABSTRACT_JOINT_MAP[name])
        else:
            expanded_problem_joints.add(name)

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

                if joint_name in expanded_problem_joints:
                    color = (0, 0, 255)  # 🔴 문제 관절
                else:
                    color = (0, 255, 0)  # 🟢 정상 관절

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
