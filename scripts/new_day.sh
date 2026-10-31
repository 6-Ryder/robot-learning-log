#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

day="${1:-$(date +%F)}"
dir="daily/$day"

mkdir -p "$dir/python" "$dir/cpp"

if [[ ! -f "$dir/README.md" ]]; then
  cat > "$dir/README.md" <<EOF
# $day

## 今天做什么

## 学到什么

## 卡住什么

## 明天第一件事
EOF
fi

echo "$dir"