# ROS 2 Robotics Logs

ROS 2 Humble / MoveIt 2 练习区，同时是 colcon 工作区根目录。

实际位置：`~/robot-learning-log/ros2robotics_logs/`；`~/ros2robotics_logs` 是指向它的软链接。文件在 git 仓库内，推送到 GitHub 后能看到具体内容（软链接本身不会被当成目录提交）。

## 环境

- ROS 2 Humble：`/opt/ros/humble`（手动 source）
- Python：`~/.venvs/ros-humble/bin/python`（3.10，`--system-site-packages`）

## 打开方式

在 VS Code 中打开本目录（`~/ros2robotics_logs` 或仓库内路径均可）。`.vscode/settings.json` 已配置解释器和 Pylance 的 ROS 包路径。

## 运行单文件脚本

```bash
./scripts/ros scripts/hello_ros.py
./scripts/ros -m pytest
```

`scripts/ros` 会 source `/opt/ros/humble/setup.bash`；本工作区构建过时，会再叠加 `install/setup.bash`。

## 创建与构建功能包

```bash
source /opt/ros/humble/setup.bash
cd src
ros2 pkg create my_pkg --build-type ament_python --dependencies rclpy --node-name my_node
cd ..
colcon build --symlink-install
```

构建后 `scripts/ros` 会自动带上新包：

```bash
./scripts/ros -c "import my_pkg; print(my_pkg.__file__)"
```

普通终端里运行节点需要先 source：

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run my_pkg my_node
```

## 调试

F5 选择 `ROS 2: Current File`。`launch.json` 注入的是基础 ROS 环境；自建包的 overlay 不会自动注入，调试自建包请用 `./scripts/ros`，或把 `install/<pkg>/lib/python3.10/site-packages` 加进 `launch.json` 的 `PYTHONPATH`。

## 目录

- `src/`：colcon 功能包
- `scripts/`：单文件练习脚本与 `ros` 运行器
- `notes/`：学习笔记