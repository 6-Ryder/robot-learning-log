# Robot Learning Log

机器人开发与 Python/C++ 学习工作区，包含每日练习、独立项目和 ROS 2 实验。

| 目录 | 用途 |
|---|---|
| `daily/` | 每日代码与日志，共享 Python 3.13 环境 |
| `exercises/` | 引导练习、测试与参考答案，使用 daily 环境 |
| `projects/` | 独立项目，各自管理环境 |
| `ros2robotics_logs/` | ROS 2 Humble / MoveIt 2，使用 Python 3.10 |
| `robotics_courses/` | 课程参考源码，获取方法见目录 README |
| `notes/` | 笔记与检查记录 |

## Python

需要 Git、uv；以下命令在仓库根目录执行。

```bash
./scripts/py.sh sync --locked --project daily
./scripts/py.sh run --locked --project daily python daily/2026-11-10/ITR01.py
./scripts/py.sh run --locked --project daily python scripts/check_daily.py

# 独立项目
./scripts/py.sh sync --locked --dev --project projects/r1-robomath
./scripts/py.sh run --locked --directory projects/r1-robomath pytest -q

# 创建当天的练习目录
./scripts/new_day.sh
```

新增依赖：`./scripts/py.sh add --project daily <包名>`。提交清单与锁文件，不提交虚拟环境。

## C++

需要 CMake ≥3.20、G++ 和 GDB；首次配置会获取 GoogleTest。

```bash
./scripts/check.sh
./build/r3/demo
```

`check.sh` 检查 r1 Python 项目，并以 Debug + ASan/UBSan 构建和测试 C++。

## ROS 2

环境准备与运行方法见 [ROS 练习区](ros2robotics_logs/README.md)。

```bash
cd ros2robotics_logs
./scripts/ros scripts/hello_ros.py
```

## 编辑器

- 普通 Python：打开 `daily/` 或具体项目目录，使用目录内的 `.venv/bin/python`。
- C++：打开仓库根目录，先运行 `scripts/check.sh` 生成编译数据库。
- ROS：单独打开 `ros2robotics_logs/`，使用该目录的解释器和调试配置。

可选：在可信终端执行 `direnv allow`，进入仓库时清理外部 Python 路径。脚本入口不依赖 direnv。
