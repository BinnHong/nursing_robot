#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """
    런치 파일의 메인 함수입니다.
    이 함수는 런치할 노드들을 정의하고 반환합니다.
    """
    return LaunchDescription([
        # NFC 리더 노드 실행
        Node(
            package='nursing_nfc_reader',
            executable='nfc_reader',
            name='nfc_reader_node',
            output='screen'
        ),
        # 여기에 추가 노드들을 정의할 수 있습니다
    ]) 