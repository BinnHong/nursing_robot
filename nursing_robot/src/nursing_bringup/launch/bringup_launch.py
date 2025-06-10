from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nursing_nfc_reader',
            executable='nfc_reader',
            name='nfc_reader_node',
            output='screen'
        )
        # 이후 아래에 추가
    ])
