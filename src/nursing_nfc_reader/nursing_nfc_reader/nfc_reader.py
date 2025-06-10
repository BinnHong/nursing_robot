import time
import board
import busio
import adafruit_pn532.i2c
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger

class NFCReaderNode(Node):
    def __init__(self):
        super().__init__('nfc_reader_node')
        self.publisher_ = self.create_publisher(String, 'nfc_id', 10)

        # I2C 초기화
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = adafruit_pn532.i2c.PN532_I2C(i2c, debug=False)
        self.pn532.SAM_configuration()

        # 서비스 등록
        self.srv = self.create_service(Trigger, 'start_nfc_read', self.handle_read_request)
        self.get_logger().info("NFC Reader Node ready.")

        # 상태 변수
        self.reading = False
        self.start_time = None

        # 타이머: 0.1초마다 상태 확인
        self.timer = self.create_timer(0.1, self.read_loop)

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


def main(args=None):
    rclpy.init(args=args)
    node = NFCReaderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()