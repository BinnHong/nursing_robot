#!/bin/bash

# 스크립트 실행 중 오류 발생시 즉시 중단
set -e

# ROS 2 Foxy 환경 설정 확인
if [ -z "$ROS_DISTRO" ] || [ "$ROS_DISTRO" != "foxy" ]; then
    echo "반드시 ROS 2 Foxy 환경에서 실행해야 합니다."
    echo "예시: source /opt/ros/foxy/setup.bash"
    exit 1
fi

echo "ROS 2 Foxy 환경에서 의존성 패키지 설치를 시작합니다..."

# 시스템 패키지 설치
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    build-essential \
    git

# Python 패키지 의존성 설치
pip3 install -r requirements.txt

# ROS 2 Foxy 의존성 설치
sudo apt-get install -y \
    ros-foxy-launch \
    ros-foxy-launch-ros \
    ros-foxy-rclpy \
    ros-foxy-std-msgs \
    ros-foxy-std-srvs

echo "의존성 패키지 설치가 완료되었습니다."

# 패키지 빌드
echo "패키지를 빌드합니다..."
colcon build --packages-select nursing_bringup nursing_nfc_reader

echo "설치가 완료되었습니다."
echo "다음 명령어로 환경을 설정하세요:"
echo "source install/setup.bash" 