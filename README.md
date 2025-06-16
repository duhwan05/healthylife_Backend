# 🧠 Healthylife 2 – AI 기반 자세분석 서비스

운동 영상을 업로드하면 자세를 분석하고, GPT를 활용한 자연어 피드백과 점수를 제공하는 **AI 기반 자세 교정 서비스**입니다.  
MediaPipe와 OpenCV를 활용한 관절 추출, GPT API 연동, AWS 기반 배포를 통해  
비전문가도 자신의 자세를 쉽게 파악하고 개선할 수 있도록 도와줍니다.

---

## 📌 프로젝트 개요

- **기간**: 2024.06 ~ 2025.06  
- **목표**: 운동 데이터를 정량화하고, 사용자 맞춤형 피드백을 자동 제공하여 자세 개선에 도움  
- **핵심 기능**:
  - 운동 영상 업로드 및 실시간 분석
  - MediaPipe 기반 관절 좌표 추출
  - GPT API 연동 자연어 피드백 제공
  - 분석 결과 저장 및 리스트 조회

---

## 🛠 기술 스택

| 구분 | 기술 |
|------|------|
| **Frontend** | Next.js, React, Tailwind CSS |
| **Backend** | Django (Python), REST API |
| **AI 분석** | MediaPipe, OpenAI GPT-4 API |
| **영상 처리** | MoviePy (업로드/변환), OpenCV (프레임 분석) |
| **Database** | SQLite |
| **배포** | AWS EC2 (Backend), S3 + CloudFront (Frontend) |
| **협업 도구** | Git, GitHub |

---

## 🔧 주요 기능 구현

### 1. 회원 및 운동 분석 기능
- Django 기반 회원가입/로그인 기능
- 사용자별 영상 업로드 및 분석 결과 리스트 조회 기능 개발

### 2. 배포 및 인프라
- React 프론트를 AWS S3 + CloudFront로 정적 호스팅  
- Django 백엔드는 EC2로 배포  
- GitHub Actions 기반 CI/CD 파이프라인 구축

### 3. 운동 분석 파이프라인
- MoviePy로 업로드 영상 처리 → OpenCV로 프레임 단위 분석  
- MediaPipe로 keypoint 추출 → GPT API로 피드백 생성  
- 점수화 및 분석 결과 저장

---

## 📸 UI 미리보기

> Web & Mobile UI 흐름은 `docs/` 폴더 혹은 [시연 영상]()을 참고하세요.

![image](https://github.com/user-attachments/assets/2a30bacf-921d-4cd1-8049-86cb96187329)

![image](https://github.com/user-attachments/assets/77fe5166-db9b-4497-a955-054cd7e86177)


---

## 🔮 개선 및 확장 가능성

- 사용자 특이사항 기반 분석 커스터마이징
- 챗봇 연동을 통한 간편 분석 기능 제공
- 자세 점수 변화 시각화 및 동기 부여 요소 강화

---

## 🙌 기여자

- **백엔드 / AI 분석**: 박두환  
- **프론트엔드**: 심준서


