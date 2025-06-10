# 🧠 nursing_bringup 패키지

`nursing_bringup`은 **환자 케어 로봇 시스템에서 필요한 ROS 2 노드들을 한 번에 실행**할 수 있도록 설계된 **통합 실행 패키지**입니다.  
NFC 리더, 내비게이션 노드 등을 launch 파일로 관리하여, 사용자가 직접 각각 실행하지 않아도 됩니다.

---

## 🚀 설치 및 실행 방법 (ROS 2 Foxy 기준)

### 1. ROS 2 Foxy 환경 설정

```bash
source /opt/ros/foxy/setup.bash
```

---

### 2. 설치 스크립트 사용

```bash
cd src/nursing_bringup
chmod +x install.sh
./install.sh
```

> `install.sh`에는 Python 패키지 설치 및 빌드 명령이 포함돼 있습니다.

---

### 3. 런치 파일 실행

```bash
source install/setup.bash
ros2 launch nursing_bringup nursing_bringup.launch.py
```

---

### 4. 직접 설치를 원하는 경우

#### Python 의존성 설치

```bash
pip3 install -r requirements.txt
```

#### ROS 2 패키지 설치

```bash
sudo apt install ros-foxy-launch ros-foxy-launch-ros ros-foxy-rclpy ros-foxy-std-msgs ros-foxy-std-srvs
```

#### 빌드

```bash
colcon build --packages-select nursing_bringup nursing_nfc_reader
```

---

## 🧩 현재 구성된 노드

현재 `nursing_bringup.launch.py` 파일에는 다음 노드가 등록되어 있습니다:

```python
Node(
    package='nursing_nfc_reader',
    executable='nfc_reader',
    name='nfc_reader_node',
    output='screen'
)
```

추후 다음과 같은 노드들이 순차적으로 추가될 예정입니다:

| 노드 파일 | 설명 |
|-----------|------|
| `navigation_launch.py` | nav2 기반 이동 처리 |
| `full_system.launch.py` | 전체 시스템 통합 실행 |

---

## 📂 디렉토리 구조

```
nursing_bringup/
├── launch/
│   └── nursing_bringup.launch.py  ← 런치 파일
├── package.xml
├── setup.py
├── install.sh                     ← 설치 스크립트
└── README.md
```

---

## 📦 관련 패키지 역할

| 패키지 이름              | 설명 |
|--------------------------|------|
| `nursing_bringup`        | 전체 시스템 노드를 실행하는 launcher |
| `nursing_nfc_reader`     | NFC 태그를 인식하고 UID를 발행 |
| `nursing_navigation` (예정) | nav2 기반 자율 이동 처리 |

---

## 👶 예시로 설명하는 포인트

- **launch 파일**은 여러 개의 노드를 동시에 실행할 수 있는 **자동화 스크립트**입니다.
- `nursing_bringup.launch.py`는 NFC 리더 노드부터 시작해 앞으로 더 많은 노드를 **한꺼번에 실행**할 수 있게 도와줍니다.
- 이 구조는 로봇의 "시동 버튼" 역할을 하며, 사용자는 복잡한 실행 명령 없이 하나의 파일로 전체 시스템을 시작할 수 있습니다.

