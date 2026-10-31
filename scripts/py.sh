#!/usr/bin/env bash
set -euo pipefail

# 本机 ~/.bashrc 会 source ROS Humble，导致 PYTHONPATH 指向
# Python 3.10 的 ROS 包；在 Python 3.13 的 uv 环境里会误加载
# ROS 的 pytest 插件。学习项目统一用这个包装器清掉。
exec env -u PYTHONPATH -u PYTEST_PLUGINS uv "$@"