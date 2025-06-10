# 🤖 Nursing Care Robot (ROS 2 Foxy)

이 프로젝트는 **환자 케어 로봇**을 위한 ROS 2 기반 시스템입니다.  
Jetson Nano를 기반으로, NFC 태그를 통한 환자 식별, 감정 점수 판단, 자율 이동 등의 기능을 구성합니다.

---

## 🧩 현재 구성된 주요 기능

| 패키지명              | 기능 설명 |
|-----------------------|-----------|
| `nursing_nfc_reader`  | PN532를 통해 NFC 태그를 인식하고 UID를 발행 |
| `nursing_bringup`     | 전체 노드 실행을 위한 launch 패키지 |
| `nursing_navigation` _(예정)_ | nav2 기반 자율 이동 노드 |

---

## 📦 설치 및 실행 (요약)

```bash
# ROS 2 Foxy 환경 준비
source /opt/ros/foxy/setup.bash

# 빌드
cd ~/ros2_ws
colcon build
source install/setup.bash

# 전체 시스템 실행
ros2 launch nursing_bringup nursing_bringup.launch.py
```

자세한 설치/구성은 각 패키지 내부의 README를 참고하세요.

---

## 🗂️ 디렉토리 구조

```
nursing_robot/
├── nursing_nfc_reader/     ← NFC 리더 노드
├── nursing_bringup/        ← 통합 launch 패키지
├── nursing_navigation/     ← nav2 연동 노드 (예정)
└── README.md               ← 최상단 요약 파일
```

---

## ✅ TODO 리스트

- [x] Jetson Nano에서 PN532로 NFC ID 감지
- [x] ROS 2 서비스 기반 NFC 노드 구성
- [x] 비블로킹 구조로 감지 요청 처리
- [x] `bringup.launch.py`로 launch 통합
- [ ] IMU 발행 노드 설계계


---

## 🧑‍💻 기여자

- 🧠 [TRAIN-Proj 팀원들](https://github.com/TRAIN-Proj)

---
