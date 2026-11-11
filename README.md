# Robot Learning Log

记录每天学习机器人开发、Python/C++ 编程的练习与笔记。

## 目录

- `daily/`：每天手写的 Python/C++ 代码与学习日志（主练习区）
- `projects/`：完整项目（独立环境）
- `ros2robotics_logs/`：ROS 2 Humble 练习区（独立 VS Code 工作区，见该目录 README）
- `exercises/`：带骨架、失败测试和参考答案的引导单元（可选题目）
- `notes/`：跨天主题笔记
- `scripts/`：日常自动化

## 快速开始

```bash
# Python 项目
cd projects/r1-robomath
uv sync --dev
env -u PYTHONPATH uv run pytest -q

# C++ 项目
cd ../..
./scripts/check.sh

# 新建今天的学习目录
./scripts/new_day.sh
```

## 环境约定

- `daily/` 是一个独立 uv 项目，所有每日练习共享 `daily/.venv`；`uv add` 加常用包。
- `projects/` 每个项目独立 `uv` 环境，互不影响。
- 一次性试包：`env -u PYTHONPATH uv run --with <pkg> python ...`，不修改 `daily/pyproject.toml`。
- C++：CMake + GoogleTest（FetchContent），构建目录统一在根目录 `build/`。
- 不提交 `.venv/`、`build/`、数据、checkpoint、密钥。

## VS Code 解释器

- 写 `daily/`：打开 `daily/` 文件夹，选 `daily/.venv/bin/python`。
- 写 `projects/r1-robomath/`：打开该项目文件夹，选它自己的 `.venv`。
- 写 C++：打开仓库根目录或 `projects/r3-minilinalg/`，CMake Tools 会自动读 `build/r3/compile_commands.json`。

## direnv 与 PYTHONPATH

仓库根目录有 `.envrc`，进入目录时自动清掉外部环境泄漏进来的 `PYTHONPATH` 和 pytest 插件变量。第一次使用：

```bash
cd ~/robot-learning-log
direnv allow
```

之后直接：

```bash
uv run --project daily python daily/2026-11-01/python/ex01.py
./scripts/check.sh
```

如果 shell 没有 direnv，再用 `env -u PYTHONPATH` 作为兜底。

## 进度

见 [progress.md](progress.md)。