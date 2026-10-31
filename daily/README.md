# daily：每天手写代码 + 学习日志

`daily/` 是你每天**亲手写** Python/C++ 的地方，也是学习日志；它不是教程仓库。

## 目录

```text
daily/2026-11-01/
├── README.md      # 今天跟的教程/项目、写了什么、测了什么、卡住什么
├── python/        # 今天手写的 Python
└── cpp/           # 今天手写的 C++
```

多天项目可以放在起始日期的目录里，例如 `daily/2026-11-04/python/traj_stats/`。

## 每天 3 小时

| 时间 | 动作 |
|---|---|
| 30 min | 读教程或开源代码，只读一小节/一个函数 |
| 90 min | 关掉教程，从空文件手写 |
| 30 min | 写测试、调试、对比输出 |
| 15 min | 写 daily README、commit |

## 每天流程

```bash
cd ~/robot-learning-log
./scripts/new_day.sh

# 在 daily/YYYY-MM-DD/README.md 写：来源、链接、目标
# 在 python/ 和 cpp/ 里手写
# 跑测试
git add daily scripts notes
git commit -m "day: $(date +%F) - 主题"
git push
```

## 2–3 周安排

| 天 | 主线 | 教程/参考 | 手写内容 |
|---|---|---|---|
| 1 | Python 函数/数据结构 | CS50P weeks 0–1；Exercism | 5 个函数 + 5 道 Exercism |
| 2 | 文件/异常 | CS50P 文件与异常 | CSV 读取器 + pytest |
| 3 | 类/模块/typing | CS50P OOP | `Record`/`Stats` 类 + 测试 |
| 4 | CLI/argparse | CS50P；pytest | `traj_stats` CLI 雏形 |
| 5 | 错误处理/重构 | 自己的代码 | CLI 完整版 + 10 个测试 |
| 6 | 复盘 + 几何 | `exercises/r1/01_se2` | 手写 SE(2) + 13 个测试 |
| 7 | C++ 工具链 | learncpp 1–2 | CMake + GoogleTest hello |
| 8 | 指针/引用/STL | learncpp 3–6；Exercism | `stats.cpp` 函数 + 5 题 |
| 9 | 类/RAII | learncpp 7–10 | `Record`/`Stats` 类 |
| 10 | STL/文件 | learncpp 11–13 | C++ `traj_stats` |
| 11 | CMake/测试/ASan | GoogleTest | 10 个测试 + ASan |
| 12 | 重构/benchmark | 自己的代码 | 与 Python 输出逐行对比 |
| 13 | SE(2)/SE(3) | `exercises/r1/01_se2`、`02_se3` | Python 几何库 |
| 14 | 四元数 | `exercises/r1/03_quaternion` | 互转/乘法 + 测试 |
| 15 | C++ Vector/Matrix | `exercises/r3/01_vector`、`02_matrix` | 规则五 + 运算符 |
| 16 | pybind11 | `exercises/r4/01_pybind11` | C++ 类暴露给 Python |
| 17 | 综合 | 自己的代码 | C++ 矩阵 + Python CLI |
| 18 | 复盘 | 一个 300 行开源文件 | 从记忆重写一个模块 + 读代码笔记 |

只有 2 周：做第 1–12 天；第 13–18 天留到第 3 周。

## 和 `exercises/` 的关系

- `daily/`：主练习区，手写代码 + 日志；
- `exercises/`：可选题目，包含 README、骨架、失败测试、参考答案；
- 推荐：先读 exercise 的 README，关掉，在 `daily/` 里从空文件写；写完再对照 `solution/`；
- 不要两边重复实现同一个东西。

## 和开源项目的关系

每天选一个**小目标**，不要 clone 一个大仓库就开始读：

- Python：CS50P 一节、Exercism 一题、PythonRobotics 一个函数；
- C++：learncpp 一节、Exercism 一题、CppRobotics 一个算法；
- 读一个函数/一节，关掉，凭记忆写；
- 不复制整段代码；写完用测试或输出对比；
- 卡住超过 2 天就简化问题，不要硬耗。

## 每天 README 模板

`scripts/new_day.sh` 会自动生成：

```markdown
# 2026-11-01

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
```