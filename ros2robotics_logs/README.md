# ROS 2 练习区

ROS 2 Humble / MoveIt 2 的 colcon 工作区。环境为 Ubuntu 22.04、系统 Python 3.10，以及 `~/.venvs/ros-humble` 专用虚拟环境。

## 准备环境

已安装 Humble 并配置 apt 软件源后，在本目录执行：

```bash
sudo apt install $(cat apt-packages.txt)
uv venv --python /usr/bin/python3 --system-site-packages ~/.venvs/ros-humble
PYTHONNOUSERSITE=1 uv pip install --python ~/.venvs/ros-humble/bin/python -r requirements.lock
```

已有环境时跳过 `uv venv`。Python 依赖入口是 `requirements.in`，锁文件由 `uv pip compile --python-version 3.10 requirements.in -o requirements.lock` 更新。ROS 包由 apt 管理。

## 运行与构建

```bash
./scripts/ros scripts/hello_ros.py
./scripts/ros scripts/check_environment.py
./scripts/ros -m pytest

source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 run <包名> <节点名>
```

功能包放在 `src/`，笔记放在 `notes/`。运行器自动加载 Humble 和本工作区的 `install/setup.bash`。

## 编辑与调试

单独打开本目录。F5 可调试基础 ROS 脚本；调试本地功能包时，在已构建的工作区运行：

```bash
./scripts/ros -m debugpy --listen 127.0.0.1:5678 --wait-for-client scripts/hello_ros.py
```

然后选择 `ROS 2: Attach`，使调试器继承运行器加载的工作区环境。
