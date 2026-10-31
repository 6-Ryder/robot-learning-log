#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

day="${1:-$(date +%F)}"
dir="daily/$day"

mkdir -p "$dir/python" "$dir/cpp"

if [[ ! -f "$dir/README.md" ]]; then
  cat > "$dir/README.md" <<EOF
# $day

## 今天跟的教程/项目
- 来源：
- 链接：
- 目标：

## 今天手写
- python/
- cpp/

## 测试结果
- pytest：
- ctest：

## 卡住
-

## 明天第一件事
-
EOF
fi

echo "$dir"