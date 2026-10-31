# 练习单元

`exercises/` 是带测试的引导题目，不是另一门课；主练习区是 `daily/`。
每个单元是一个可独立运行的小教程：

```text
<unit>/
  README.md        # 概念、推导、任务、提示、自测问题
  <module>.py      # 骨架：TODO / NotImplementedError
  test_<module>.py # 一开始全红，实现后变绿
  solution/        # 参考实现；先自己写完再看
```

运行方式（以 R1-01 为例）：

```bash
cd ~/robot-learning-log/exercises/r1/01_se2
uv run --project ../../../daily pytest -q
```

## 单元清单

| 单元 | 主题 | 状态 |
|---|---|---|
| `r1/01_se2` | SE(2)：旋转、平移、compose、inverse、点变换 | ✅ 可用 |
| `r1/02_se3` | SE(3)：3D 旋转、齐次变换、点变换 | 待生成 |
| `r1/03_quaternion` | 四元数：互转、乘法、归一化 | 待生成 |
| `r1/04_fk_jacobian` | 二连杆 FK、几何雅可比、有限差分验证 | 待生成 |
| `r1/05_ik` | 阻尼最小二乘 IK、奇异位形 | 待生成 |
| `r1/06_trajectory` | 线性/三次/五次插值、数值微分 | 待生成 |
| `r3/01_vector` | C++ Vector：构造、访问、norm、异常、GoogleTest | 待生成 |
| `r3/02_matrix` | C++ Matrix：运算符、规则五、维度检查 | 待生成 |
| `r3/03_rk4_pendulum` | RK4、单摆、能量检查 | 待生成 |
| `r3/04_pid_lqr` | PID、有限差分线性化、LQR | 待生成 |
| `r4/01_pybind11` | 暴露 C++ 类给 Python | 待生成 |
| `r4/02_control_loop` | 1 kHz 循环、延迟、jitter | 待生成 |

## 学习方式

1. 读 `README.md` 的概念和任务；
2. 只改骨架文件，不打开 `solution/`；
3. 跑 pytest，一次让一个测试变绿；
4. 全绿后回答自测问题；
5. 再看 `solution/`，对照实现差异；
6. commit，例如 `feat(r1-01): implement se2 transforms`。

## 为什么不是把教程写成一个大 Markdown

- 代码要能运行、测试要能失败/通过，Markdown 里的代码块做不到；
- 每个单元独立目录，方便你只提交自己的实现；
- 参考答案分开，避免“看一遍就算学会”；
- 以后加 C++ 单元时，目录结构一致。