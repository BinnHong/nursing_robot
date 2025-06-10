from setuptools import setup

package_name = 'nursing_nfc_reader'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jetson',
    maintainer_email='jetson@todo.todo',
    description='NFC 태그를 읽고 토픽/서비스로 응답하는 노드',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nfc_reader = nursing_nfc_reader.nfc_reader:main',
        ],
    },
)
