#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Python: r1-robomath =="
(cd projects/r1-robomath && env -u PYTHONPATH -u PYTEST_PLUGINS uv run pytest -q)

echo "== C++: r3-minilinalg =="
cmake -S projects/r3-minilinalg -B build/r3 \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"
cmake --build build/r3 -j
ctest --test-dir build/r3 --output-on-failure

echo "All checks passed."