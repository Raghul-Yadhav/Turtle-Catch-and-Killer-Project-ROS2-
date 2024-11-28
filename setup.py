from setuptools import find_packages, setup

package_name = 'turtle_catcher'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='raggy2k',
    maintainer_email='raggy2k@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "turtle_controller = turtle_catcher.turtle_controller:main",
            "turtle_spawner = turtle_catcher.turtle_spawner:main",
            "control_turtle = turtle_catcher.control_turtle:main",
            "spawn_turtle = turtle_catcher.spawn_turtle:main"
        ],
    },
)
