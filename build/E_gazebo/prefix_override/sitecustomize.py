import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/edu19/robot_navigation/colcon_ws/install/E_gazebo'
