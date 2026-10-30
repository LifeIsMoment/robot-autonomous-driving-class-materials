# a_pubsub

This ROS 2 package simulates a 2D position using keyboard input. No robot
hardware is required; the three ROS 2 nodes exchange messages locally:

- `publisher` reads `w`, `a`, `s`, or `d`, then publishes a movement command
  after Enter is pressed.
- `processor` applies each command to a position that starts at `(0, 0)`.
- `subscriber` prints each position message it receives.

The directions are `w` = +y, `a` = -x, `s` = -y, and `d` = +x.
The processor publishes the position every 0.5 seconds, so the subscriber may
print the same position more than once between movement commands.

## Build

From the workspace root, with the ROS 2 environment sourced:

```bash
colcon build --base-paths src --packages-select a_pubsub
source install/setup.bash
```

## Run

Start each node in a separate terminal, in this order:

```bash
ros2 run a_pubsub subscriber
ros2 run a_pubsub processor
ros2 run a_pubsub publisher
```

The publisher needs an interactive terminal. Type one direction and press
Enter to send it. Use `Ctrl+C` to stop a node.

The nodes communicate on `/direction` (`std_msgs/String`) and `/location`
(`std_msgs/Int16MultiArray`).

Alternatively, start all three nodes from one terminal with:

```bash
ros2 launch a_pubsub pubsub.launch.py
```
