# nursing\_nfc\_reader 패키지

이 패키지는 **Jetson Nano에서 NFC 태그를 읽기 위한 ROS 2 노드**를 제공합니다. PN532 모듈을 I2C 방식으로 연결하여, 서비스 요청이 들어오면 NFC 태그를 읽고 그 값을 토픽으로 발행합니다.

---

## 🧩 주요 기능

* **항상 실행되는 NFC 노드**
* ROS 2 서비스 `/start_nfc_read`를 통해 NFC 태그 인식 요청
* 최대 10초 동안 태그를 감지하고, 성공 시 `/nfc_id` 토픽에 UID(고유 식별자)를 발행
* 실패 시 아무 값도 보내지 않고 로그 출력

---

## 📦 토픽 & 서비스

| 항목    | 이름                | 설명                                |
| ----- | ----------------- | --------------------------------- |
| ✅ 서비스 | `/start_nfc_read` | 태그 읽기 시작 요청 (`std_srvs/Trigger`)  |
| ✅ 토픽  | `/nfc_id`         | 태그 UID를 `std_msgs/String` 타입으로 발행 |

---

## 🚀 실행 방법

### 1. NFC 리더 노드 실행

```bash
ros2 run nursing_nfc_reader nfc_reader
```

### 2. 태그 감지 요청 (다른 터미널에서 실행)

```bash
ros2 service call /start_nfc_read std_srvs/srv/Trigger
```

### 3. 결과 확인

* 성공 시: `/nfc_id` 토픽에서 UID 수신 가능
* 실패 시: "10초 초과" 메시지 출력됨

---

## 🤝 nursing_bringup 런치 연동 예시

nursing_bringup 패키지의 런치 파일에서 아래와 같이 이 노드를 자동 실행할 수 있습니다:

```python
Node(
    package='nursing_nfc_reader',
    executable='nfc_reader',
    name='nfc_reader',
    output='screen'
)
```

---

## 🔌 하드웨어 연결 방법 (Jetson Nano + PN532)

### 📍 배선 연결 (I2C 기준)

| PN532 핀 | Jetson Nano 40핀 헤더   | 설명            |
| ------- | -------------------- | ------------- |
| VCC     | 1번 (3.3V) 또는 2번 (5V) | 전원 공급 (5V 권장) |
| GND     | 6번                   | 접지            |
| SDA     | 3번 (I2C 데이터)         | I2C 데이터 핀     |
| SCL     | 5번 (I2C 클럭)          | I2C 클럭 핀      |

### 🔧 PN532 DIP 스위치 설정

* 보드의 통신 모드 설정 스위치를 다음과 같이 설정해야 합니다:

  * `I2C 모드`: DIP 스위치 → **H-L**
  * ->`SET0=H`, `SET1=L`

### ✅ 확인 방법

```bash
sudo i2cdetect -r -y 1
```

* PN532가 연결되어 있다면 `0x24` 또는 `0x48` 등으로 감지됨

---

## 📁 코드 요약 및 주요 함수 예시

* `nfc_reader.py`:

  * I2C를 통해 PN532 초기화
  * 서비스 요청이 오면 내부 플래그를 켜고 10초간 감지 루프 실행
  * 감지 성공 시 UID를 발행하고 대기 상태로 복귀

### 서비스 콜백 및 토픽 발행 예시 (실제 코드)

```python
class NFCReaderNode(Node):
    def __init__(self):
        # ... (생략)
        self.publisher_ = self.create_publisher(String, 'nfc_id', 10)
        self.srv = self.create_service(Trigger, 'start_nfc_read', self.handle_read_request)
        # ... (생략)

    def handle_read_request(self, request, response):
        if self.reading:
            response.success = False
            response.message = '이미 태그 감지 중입니다.'
        else:
            self.reading = True
            self.start_time = time.time()
            response.success = True
            response.message = '태그 감지를 시작합니다.'
            self.get_logger().info("[서비스] 태그 감지 시작")
        return response

    def read_loop(self):
        if not self.reading:
            return
        # 최대 10초까지 시도
        if time.time() - self.start_time > 10.0:
            self.get_logger().warn("태그 감지 실패 (10초 초과)")
            self.reading = False
            return
        uid = self.pn532.read_passive_target(timeout=0.1)
        if uid:
            uid_str = ''.join(f'{b:02X}' for b in uid)
            self.publisher_.publish(String(data=uid_str))
            self.get_logger().info(f"[성공] 태그 감지됨: {uid_str}")
            self.reading = False
```

---

## 🧠 예시 응답 결과

```bash
$ ros2 topic echo /nfc_id
---
data: "04A3BC2F77"
```

---

## 🛠️ 설치 전제 조건

* ROS 2 Foxy 환경
* PN532 NFC 모듈 (I2C 모드 설정)
* Python 라이브러리:

  ```bash
  pip3 install adafruit-circuitpython-pn532
  ```

---

## 📌 참고 사항

* PN532 모듈의 DIP 스위치를 반드시 I2C 모드로 설정해야 합니다.
* Jetson Nano는 기본적으로 `/dev/i2c-1`을 사용하며, 이 포트는 I2C용으로 미리 열려 있어야 합니다.
* PN532의 LED가 켜지지 않거나 i2cdetect에 주소가 안 뜨면 배선, 전원, 모드 설정을 다시 점검하세요.

---

## 👶 예시로 설명하는 포인트

* **서비스 요청**은 "시작 버튼" 역할입니다. NFC를 읽어달라고 말하는 것이고,
* **토픽 발행**은 "결과 방송"입니다. 태그를 읽으면 해당 내용을 공개하는 개념입니다.
* 이 노드는 항상 실행되며, 요청이 있을 때만 작동하는 똑똑한 감시자입니다.
* PN532는 NFC 태그(예: MIFARE 카드, 스마트폰)에서 UID를 읽는 장치입니다.

