# R1-01：SE(2) 变换

这是 R1 `robomath` 的第一个练习单元。目标不是“看懂”，而是**从空文件写出 SE(2) 的 compose、inverse、transform_point**，并用测试验证。

## 数学背景

二维刚体变换可以写成：

```text
T = [ R  t ]      R 是 2x2 旋转矩阵，t 是 2x1 平移
    [ 0  1 ]
```

旋转矩阵：

```text
R(theta) = [ cosθ  -sinθ ]
           [ sinθ   cosθ ]
```

组合（先做 `other`，再做 `self`）：

```text
T1 ∘ T2 = [ R1 R2   R1 t2 + t1 ]
```

逆：

```text
T^-1 = [ R^T   -R^T t ]
```

## 任务

在 `se2.py` 中实现：

1. `rotation(theta)`：返回 2x2 旋转矩阵。
2. `SE2.__post_init__`：校验 `R` 是 `(2,2)`、`t` 是 `(2,)`，否则抛 `ValueError`。
3. `SE2.compose(other)`：返回组合变换。
4. `SE2.inverse()`：返回逆变换。
5. `SE2.transform_point(p)`：变换一个二维点。
6. `SE2.as_matrix()`：返回 3x3 齐次矩阵。
7. `SE2.identity()`：单位变换。
8. `SE2.from_pose(x, y, theta)`：从位姿构造。
9. `transform_points(T, points)`：一次变换 `(N,2)` 个点，必须用 NumPy 向量化，不能写 for 循环。
10. `chain(transforms)`：按顺序组合列表中的变换。

## 怎么跑

```bash
cd ~/robot-learning-log/exercises/r1/01_se2
uv run --project ../../../daily pytest -q
```

一开始应该看到 13 个测试全部失败（`NotImplementedError`）。每实现一个函数，就有一部分变绿。

## 提示

- 矩阵乘法用 `@`，不要用 `*`。
- `inverse` 不要用 `np.linalg.inv`；用 `R.T` 和 `-R.T @ t`，这是 SE(2) 的结构。
- `transform_points` 可以用 `points @ T.R.T + T.t`。
- `chain([])` 应返回单位变换。
- 不要 import `scipy.spatial.transform` 或 `pinocchio`；这个练习就是手写。

## 自测问题

做完后回答：

1. 为什么 `T1.compose(T2)` 的平移是 `R1 @ t2 + t1`，而不是 `t1 + t2`？
2. 为什么 SE(2) 的逆可以用 `R.T`，而一般 3x3 矩阵不行？
3. `transform_points` 里为什么用 `points @ T.R.T`，而不是 `T.R @ points`？形状分别是什么？

## 参考答案

`solution/se2.py`。先自己写完、测试全绿，再看答案。对照时重点看：

- `__post_init__` 的校验方式；
- `inverse` 有没有用 `np.linalg.inv`；
- `transform_points` 是否向量化。

## 验收

- 13 个测试全过；
- 没有 import 任何机器人/科学计算库（只用 NumPy 和标准库）；
- 能回答上面三个问题；
- 代码提交到 `exercises/r1/01_se2/`，commit message 例如 `feat(r1-01): implement se2 transforms`。