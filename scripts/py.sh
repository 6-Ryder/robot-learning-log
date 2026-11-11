#!/usr/bin/env bash
set -euo pipefail

# 清除外部 Python/ROS 环境，始终使用显式指定项目的 uv 环境。
exec env -u PYTHONPATH -u PYTHONHOME -u PYTEST_PLUGINS \
  -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PYTHONNOUSERSITE=1 uv "$@"
