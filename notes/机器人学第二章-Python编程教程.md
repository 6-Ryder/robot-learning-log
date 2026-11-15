# 《机器人学导论》第二章：Python 编程教程

适用情况：已经学完第二章“空间描述和变换”，希望不用 MATLAB，自己写代码计算。本文覆盖这一章需要的 Python 编程基础，并不试图讲完整门 Python 语言或后续机器人运动学课程。

学习方法：每次读一节，先预测输出，再运行代码，然后修改一个参数。能不看答案重新写出来，才算掌握。**本文每个 Python 代码块都可以独立运行，不依赖前面的变量。** 实践中你可以将代码复制到现有的学习文件，或在 Python 交互终端中执行。

## 目录

1. 环境、运行方法与包的分工
2. Python 最小基础：变量、列表、函数、循环、判断
3. NumPy 数组、维度与切片
4. 向量、矩阵与浮点数
5. 三角函数与角度
6. 旋转矩阵与坐标映射
7. 固定轴、运动轴与旋转顺序
8. 平移与齐次变换
9. 逆变换
10. 变换连乘与变换方程
11. 点和自由矢量
12. RPY 与 ZYZ 欧拉角
13. 等效角轴与四元数
14. SpatialMath 对象写法
15. 批量处理点与可视化
16. 综合案例：相机坐标转换到机器人基座
17. 常见错误与速查
18. 独立练习、参考答案与学习顺序

## 1. 环境、运行方法与包的分工

工作空间已有 `daily/.venv`，本教程无需新建环境。在仓库根目录运行现有学习文件，例如：

```bash
./scripts/py.sh run --locked --project daily python daily/2026-11-10/Math.py
```

这条命令会运行整个文件，包括你原来写在里面的代码。编辑器选择的解释器应为：

```text
/home/ryder/robot-learning-log/daily/.venv/bin/python
```

如果想一段一段输入，可以从仓库根目录启动交互终端：

```bash
./scripts/py.sh run --locked --project daily python
```

看到 `>>>` 后输入 Python 代码，退出使用 `exit()`。代码块里的内容才是程序，不要把 Markdown 的三个反引号或 `>>>` 一起复制进去。下面用这个小程序检查解释器和导入位置：

```python
import sys
import numpy as np
from spatialmath import SO3, SE3
from spatialmath.base import rpy2r, tr2rpy

print("解释器：", sys.executable)
print("NumPy：", np.__version__)
print("单位旋转：\n", SO3().A)
print("单位位姿：\n", SE3().A)
```

这些工具的分工：

| 工具 | 本教程中的用途 | 常见导入 |
|---|---|---|
| NumPy | 数组和数值运算 | `import numpy as np` |
| SpatialMath 的类 | 旋转与位姿对象 | `from spatialmath import SO3, SE3` |
| SpatialMath 基础函数 | RPY 等转换 | `from spatialmath.base import rpy2r, tr2rpy` |
| Robotics Toolbox | 后续的机器人模型、运动学等 | `import roboticstoolbox as rtb` |
| Matplotlib | 绘图 | `import matplotlib.pyplot as plt` |

安装 Robotics Toolbox 会带上配套依赖，但函数仍按所属模块导入。第二章多数计算只用 NumPy 和 SpatialMath 就够了。

## 2. Python 最小基础

### 2.1 变量、数字与列表

```python
distance = 2.0       # 浮点数
count = 3            # 整数
name = "camera"      # 字符串
enabled = True       # 布尔值，首字母大写
angles = [0, 30, 90] # Python 列表

print(distance + 1)
print(distance / count)
print(count ** 2)    # 幂运算；^ 不是乘方
print(angles[0])     # 下标从 0 开始

angles[1] = 45       # 修改列表的第 2 个元素
print(angles)
```

`=` 是赋值；`==` 才是判断相等。`#` 后面是注释，不参与运行。变量名应说明含义，如 `p_camera` 比 `a` 容易理解。

### 2.2 函数、循环、判断和断言

```python
import numpy as np


def degree_to_radian(angle_deg):
    """输入角度，返回弧度。"""
    angle_rad = angle_deg * np.pi / 180
    return angle_rad


for angle in [0, 30, 90]:
    result = degree_to_radian(angle)
    print(f"{angle} 度 = {result:.4f} 弧度")

if np.isclose(degree_to_radian(180), np.pi):
    print("转换正确")
else:
    print("检查公式")

assert np.isclose(degree_to_radian(180), np.pi)
```

逐项理解：

- `def` 定义函数，括号中是输入参数，`return` 返回结果。
- 冒号后的函数体、循环体、判断分支用 4 个空格缩进。
- `for` 会让列表中的每个值依次参与计算。
- `f"...{result:.4f}..."` 将变量放入字符串，并显示 4 位小数。
- `assert 条件` 用于自检；条件为假时会抛出 `AssertionError`。

先学会写短函数，暂时不需要自定义类。

## 3. NumPy 数组、维度与切片

### 3.1 一维数组与列向量

```python
import numpy as np

v = np.array([1., 2., 3.])
v_col = np.array([[1.], [2.], [3.]])
v_row = np.array([[1., 2., 3.]])

print(v.shape)      # (3,)
print(v_col.shape)  # (3, 1)
print(v_row.shape)  # (1, 3)
print(v.T.shape)    # (3,)：一维数组的转置不会变成行向量

print(v.reshape(3, 1))
print(v_col.ravel())  # 展平成一维数组
```

本教程主要采用 `(3,)` 表示三维坐标，采用 `(3, 3)` 表示旋转矩阵。`R @ v` 的结果仍为 `(3,)`，很适合基础运算。

不要随意把 `(3,)` 和 `(3, 1)` 混着相加：NumPy 的广播机制可能产生 `(3, 3)` 的结果，而不是报错。遇到奇怪结果，第一步就是 `print(变量.shape)`。

### 3.2 索引、切片与单位矩阵

```python
import numpy as np

M = np.array([
    [1., 2., 3.],
    [4., 5., 6.],
    [7., 8., 9.]
])

print(M[0, 1])   # 第 1 行第 2 列：2
print(M[0, :])   # 第 1 行
print(M[:, 0])   # 第 1 列
print(M[:2, :2]) # 前 2 行、前 2 列，结束下标不包含在内

T = np.eye(4)     # 4×4 单位阵
T[:3, 3] = [1, 2, 3]
print(T)

N = M.copy()     # 明确复制数据
N[0, 0] = 100
assert M[0, 0] == 1
```

`N = M` 只是让两个名字指向同一个数组；`M.copy()` 才能获得独立的数据。普通切片往往也是原数组的视图，想独立修改时也应复制。

数组细节可查 [NumPy 官方入门](https://numpy.org/doc/stable/user/absolute_beginners)。

## 4. 向量、矩阵与浮点数

```python
import numpy as np

a = np.array([1., 2., 3.])
b = np.array([4., 5., 6.])
M = np.array([[1., 2., 0.], [0., 1., 0.], [0., 0., 1.]])

print("相加：", a + b)             # [5, 7, 9]
print("标量乘法：", 2 * a)         # [2, 4, 6]
print("逐元素乘法：", a * b)       # [4, 10, 18]
print("点积：", a @ b)             # 32
print("叉积：", np.cross(a, b))    # [-3, 6, -3]
print("长度：", np.linalg.norm(a))
print("单位向量：", a / np.linalg.norm(a))
print("矩阵乘向量：", M @ a)       # [5, 2, 3]
print("矩阵乘矩阵：\n", M @ M)
print("转置：\n", M.T)

M_inv = np.linalg.inv(M)
assert np.allclose(M_inv @ M, np.eye(3), atol=1e-10)

# 浮点数不能总用 == 判断。
print(0.1 + 0.2 == 0.3)             # 通常为 False
assert np.isclose(0.1 + 0.2, 0.3)
```

本教程中最容易混淆的两个操作：**NumPy 数组的 `@` 是矩阵乘法，`*` 是逐元素乘法。**

`np.isclose` 比较数值，`np.allclose` 比较数组；默认有相对容差和绝对容差。严格检查小误差时可以指定 `rtol=0, atol=1e-10`。这里的 `1e-10` 表示 $10^{-10}$。

求单位向量前应保证长度不为零。只有方阵且可逆时，才能用 `np.linalg.inv`。求解 `M @ x = b` 时通常直接用 `np.linalg.solve(M, b)`。

## 5. 三角函数与角度

```python
import numpy as np

theta = np.deg2rad(30)
print(np.sin(theta))   # 约 0.5
print(np.cos(theta))   # 约 0.8660
print(np.rad2deg(theta))

x, y = -1., 1.
angle = np.arctan2(y, x)  # 注意先 y 后 x
print(np.rad2deg(angle))  # 135 度

# 反三角函数前处理浮点越界：1.000000000001 不是合法的 arccos 输入。
cos_value = 1.000000000001
safe_angle = np.arccos(np.clip(cos_value, -1., 1.))
assert np.isclose(safe_angle, 0)
```

NumPy 的三角函数默认使用弧度。`np.arctan2(y, x)` 能区分象限，比 `np.arctan(y / x)` 更适合恢复方向角，也避免直接除以零。

## 6. 旋转矩阵与坐标映射

统一约定：

- 使用右手坐标系、列向量和右手正角方向。
- `R_AB` 对应课本的 ${}^A R_B$，表示 B 相对于 A 的姿态。
- `p_B` 是同一个点在 B 中的坐标。
- `p_A = R_AB @ p_B` 将 B 中的坐标转换到 A；本节原点重合。
- `R_AB` 的三列是 B 的 x、y、z 轴在 A 中的表示。

三个基本旋转矩阵如下，输入统一为弧度：

```python
import numpy as np


def rot_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1., 0., 0.], [0., c, -s], [0., s, c]])


def rot_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0., s], [0., 1., 0.], [-s, 0., c]])


def rot_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0.], [s, c, 0.], [0., 0., 1.]])


R_AB = rot_z(np.deg2rad(90))
p_B = np.array([1., 0., 0.])
p_A = R_AB @ p_B

print("p_A =", p_A)  # 约 [0, 1, 0]
print("B 的 x 轴在 A 中：", R_AB[:, 0])
assert np.allclose(p_A, [0, 1, 0], atol=1e-10)

# 合法旋转矩阵满足正交性与行列式为 +1。
assert np.allclose(R_AB.T @ R_AB, np.eye(3), atol=1e-10)
assert np.isclose(np.linalg.det(R_AB), 1)

# 原点重合时，逆向坐标映射使用转置。
assert np.allclose(R_AB.T @ p_A, p_B)
```

旋转矩阵既能用于坐标映射，也能作为主动旋转算子。区别在含义：坐标映射描述同一个点在不同坐标系中的分量；主动旋转描述固定参考系中一个向量被转到新方向。计算前先说清楚自己在做哪一种。

练习：用三个函数分别计算 x、y、z 轴旋转 90° 对 `[1, 0, 0]` 的作用。先画方向，再运行。

## 7. 固定轴、运动轴与旋转顺序

在矩阵作用于右侧列向量时，最右侧的运算先执行。主动地先绕固定 x 轴转，再绕固定 z 轴转，应写 `Rz @ Rx`。

如果 `R` 表示物体相对世界的当前姿态：

- 绕世界固定轴施加增量 `Q`：`R_new = Q @ R`。
- 绕物体当前自身轴施加增量 `Q`：`R_new = R @ Q`。

这里的 `Q` 必须分别在世界轴或物体自身轴下定义；不要脱离参考系机械记忆“左乘/右乘”。

```python
import numpy as np
from spatialmath import SO3

Rx = SO3.Rx(90, unit="deg").A
Rz = SO3.Rz(90, unit="deg").A
v = np.array([0., 1., 0.])

print("先固定 x，后固定 z：", Rz @ Rx @ v)  # 约 [0, 0, 1]
print("先固定 z，后固定 x：", Rx @ Rz @ v)  # 约 [-1, 0, 0]
assert not np.allclose(Rz @ Rx, Rx @ Rz)

R_current = Rz
R_world_x = Rx @ R_current
R_body_x = R_current @ Rx
assert not np.allclose(R_world_x, R_body_x)
```

旋转一般不可交换。这不是 Python 特性，而是空间旋转本身的性质。

## 8. 平移与齐次变换

`t_AB` 表示 B 原点在 A 中的位置。点的坐标映射为：

$$p_A=R_{AB}p_B+t_{AB}.$$

把它写成一次矩阵乘法：

$$T_{AB}=\begin{bmatrix}R_{AB}&t_{AB}\\0&1\end{bmatrix},\qquad
\begin{bmatrix}p_A\\1\end{bmatrix}=T_{AB}\begin{bmatrix}p_B\\1\end{bmatrix}.$$

```python
import numpy as np
from spatialmath import SO3

R_AB = SO3.Rz(90, unit="deg").A
t_AB = np.array([1., 2., 0.])
p_B = np.array([1., 0., 0.])

p_A = R_AB @ p_B + t_AB

T_AB = np.eye(4)
T_AB[:3, :3] = R_AB
T_AB[:3, 3] = t_AB

p_B_h = np.append(p_B, 1.)
p_A_h = T_AB @ p_B_h

print("T_AB =\n", T_AB)
print("p_A =", p_A_h[:3])  # 约 [1, 3, 0]
assert np.allclose(p_A_h[:3], p_A)
assert np.allclose(p_A, [1, 3, 0])
assert np.isclose(p_A_h[3], 1)
```

`T[:3, :3]` 取旋转，`T[:3, 3]` 取平移。刚体齐次变换的最后一行必须为 `[0, 0, 0, 1]`。

本教程距离单位统一为米。NumPy 不会替你检查单位；把毫米数据直接混进米的数据里，程序可能正常运行但结果错误。

## 9. 逆变换

逆变换把 A 中的坐标变回 B：

$$T_{BA}=T_{AB}^{-1}=\begin{bmatrix}R_{AB}^T&-R_{AB}^Tt_{AB}\\0&1\end{bmatrix}.$$

**旋转矩阵的逆等于转置，但整个齐次变换的逆通常不等于转置。**

```python
import numpy as np
from spatialmath import SE3


def inverse_transform(T):
    R = T[:3, :3]
    t = T[:3, 3]
    result = np.eye(4)
    result[:3, :3] = R.T
    result[:3, 3] = -R.T @ t
    return result


T_AB = (SE3(1, 2, 0) * SE3.Rz(90, unit="deg")).A
T_BA = inverse_transform(T_AB)
p_B_h = np.array([1., 0., 0., 1.])
p_A_h = T_AB @ p_B_h

print("恢复 B 中坐标：", (T_BA @ p_A_h)[:3])
assert np.allclose(T_BA @ p_A_h, p_B_h)
assert np.allclose(T_BA @ T_AB, np.eye(4), atol=1e-10)
assert np.allclose(T_BA, np.linalg.inv(T_AB))
```

先掌握分块求逆的公式，再用库函数简化。上面的函数假定输入是合法的刚体变换，不能用于任意 4×4 矩阵。

## 10. 变换连乘与变换方程

如果有 A、B、C 三个坐标系：

$$T_{AC}=T_{AB}T_{BC}.$$

右侧先执行 C→B，再执行 B→A。中间坐标系下标相接，是检查顺序的好方法。

```python
import numpy as np
from spatialmath import SE3

T_AB = (SE3(1, 2, 0) * SE3.Rz(90, unit="deg")).A
T_BC = SE3(1, 0, 0).A
T_AC = T_AB @ T_BC

p_C_h = np.array([1., 0., 0., 1.])
p_A_h = T_AC @ p_C_h
print("p_A =", p_A_h[:3])  # 约 [1, 4, 0]
assert np.allclose(p_A_h, T_AB @ (T_BC @ p_C_h))
assert np.allclose(p_A_h[:3], [1, 4, 0])

# 已知 T_AB、T_AC，求 T_BC：解 T_AB @ X = T_AC。
T_BC_found = np.linalg.solve(T_AB, T_AC)
assert np.allclose(T_BC_found, T_BC)

# 已知 T_AC、T_BC，求 T_AB：右乘 T_BC 的逆。
T_AB_found = T_AC @ np.linalg.inv(T_BC)
assert np.allclose(T_AB_found, T_AB)

# 闭环一致性：A→C→B→A。
T_CA = np.linalg.inv(T_AC)
assert np.allclose(T_AB @ T_BC @ T_CA, np.eye(4), atol=1e-10)
```

矩阵方程不能像普通数字一样随意移项。左侧因子要在左侧消去，右侧因子要在右侧消去。

如果已知 `T_AB` 和 `T_AC`，要求 C 在 B 中的位姿，应计算 `T_BC`；不要只凭“这两个矩阵相乘看看”来试顺序。

## 11. 点和自由矢量

点的位置受旋转和平移影响；自由矢量没有固定起点，只受旋转影响。方向、速度方向等可以按自由矢量变换，但不要把附带参考点的力矩等直接当作这里的简单自由矢量处理。

```python
import numpy as np
from spatialmath import SE3

T_AB = (SE3(1, 2, 0) * SE3.Rz(90, unit="deg")).A

p_B_h = np.array([1., 0., 0., 1.])  # 点：末位 1
v_B_h = np.array([1., 0., 0., 0.])  # 自由矢量：末位 0

p_A_h = T_AB @ p_B_h
v_A_h = T_AB @ v_B_h

print("点：", p_A_h[:3])         # [1, 3, 0]
print("自由矢量：", v_A_h[:3])   # [0, 1, 0]
assert np.allclose(v_A_h[:3], T_AB[:3, :3] @ v_B_h[:3])
```

## 12. RPY 与 ZYZ 欧拉角

### 12.1 明确 RPY 的定义

本教程使用：

$$R=R_z(yaw)R_y(pitch)R_x(roll).$$

对应 SpatialMath 的 `order="zyx"`，但输入列表仍是 `[roll, pitch, yaw]`，不能把列表倒成 `[yaw, pitch, roll]`。

```python
import numpy as np
from spatialmath import SO3
from spatialmath.base import rpy2r, tr2rpy

rpy_deg = [10., 20., 30.]
R = rpy2r(rpy_deg, unit="deg", order="zyx")
R_manual = (SO3.Rz(30, unit="deg").A
            @ SO3.Ry(20, unit="deg").A
            @ SO3.Rx(10, unit="deg").A)

recovered = tr2rpy(R, unit="deg", order="zyx")
print("恢复的 RPY：", recovered)  # 约 [10, 20, 30]
assert np.allclose(R, R_manual)
assert np.allclose(rpy2r(recovered, unit="deg", order="zyx"), R)

# 对本例这种非奇异情况，也可以直接从矩阵元素恢复一个角解。
roll = np.arctan2(R[2, 1], R[2, 2])
pitch = np.arctan2(-R[2, 0], np.hypot(R[0, 0], R[1, 0]))
yaw = np.arctan2(R[1, 0], R[0, 0])
print("手动恢复：", np.rad2deg([roll, pitch, yaw]))
```

这里的手算公式选择了俯仰角位于 `[-90°, 90°]` 的分支。俯仰角为 ±90° 时出现奇异性，不能靠这几行唯一恢复 roll 和 yaw。

姿态角可能有多组解。检查转换是否正确时，优先比较重新生成的旋转矩阵，而不是要求角度列表逐项相同。接口和约定参见 [SpatialMath 三维转换函数](https://spatialmath-python.rai-inst.com/func_3d.html)。

### 12.2 ZYZ 欧拉角

这里单独使用 ZYZ 约定：

$$R=R_z(\alpha)R_y(\beta)R_z(\gamma).$$

```python
import numpy as np
from spatialmath import SO3

R = SO3.Eul([30, 40, 50], unit="deg")
angles = R.eul(unit="deg")
print("ZYZ 欧拉角：", angles)

manual = (SO3.Rz(30, unit="deg").A
          @ SO3.Ry(40, unit="deg").A
          @ SO3.Rz(50, unit="deg").A)
assert np.allclose(R.A, manual)
assert np.allclose(SO3.Eul(angles, unit="deg").A, R.A)
```

`Eul` 创建对象，`eul` 从对象提取角度；大小写有区别。不能看到“欧拉角”三个字就忽略轴顺序。RPY 和这里的 ZYZ 是两套不同约定，角度不能直接混用。

## 13. 等效角轴与四元数

### 13.1 等效角轴与 Rodrigues 公式

给定单位轴 $k$ 与角度 $\theta$：

$$R=I+\sin\theta[k]_\times+(1-\cos\theta)[k]_\times^2.$$

```python
import numpy as np
from spatialmath import SO3

axis = np.array([1., 1., 0.])
axis = axis / np.linalg.norm(axis)
theta = np.deg2rad(60)
x, y, z = axis

K = np.array([[0., -z, y], [z, 0., -x], [-y, x, 0.]])
R_manual = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
R_object = SO3.AngVec(theta, axis)
angle_back, axis_back = R_object.angvec()

print("角度（度）：", np.rad2deg(angle_back))
print("单位轴：", axis_back)
assert np.allclose(R_manual, R_object.A)
assert np.allclose(SO3.AngVec(angle_back, axis_back).A, R_manual)
```

输入轴不能为零向量。零旋转的轴不唯一，180° 附近手动恢复轴也要特别处理；基础阶段先掌握构造与使用经过验证的库函数。

### 13.2 单位四元数

按标量在前的约定：

$$q=[w,x,y,z]=[\cos(\theta/2),\;k\sin(\theta/2)].$$

```python
import numpy as np
from spatialmath import SO3, UnitQuaternion

theta = np.deg2rad(90)
axis = np.array([0., 0., 1.])
q_manual = np.concatenate(([np.cos(theta / 2)], axis * np.sin(theta / 2)))

q = UnitQuaternion(SO3.Rz(90, unit="deg"))
print("手算 [w,x,y,z]：", q_manual)
print("库的 [w,x,y,z]：", q.vec)
print("旋转矩阵：\n", q.SO3().A)

assert np.isclose(np.linalg.norm(q_manual), 1)
assert np.allclose(q.SO3().A, SO3.Rz(90, unit="deg").A)
assert np.allclose(UnitQuaternion(-q.vec).SO3().A, q.SO3().A)
```

SpatialMath 的 `q.vec` 使用 `[w,x,y,z]`。其他库可能使用 `[x,y,z,w]`，交换数据前必须检查。`q` 与 `-q` 表示同一个旋转，不能只靠四元数分量直接相等判断姿态是否相同。参见 [SpatialMath 单位四元数文档](https://spatialmath-python.rai-inst.com/3d_orient_unitquaternion.html)。

## 14. SpatialMath 对象写法

手写矩阵能帮助理解，熟悉后可以用对象完成常见计算。

```python
import numpy as np
from spatialmath import SO3, SE3

R = SO3.Rz(90, unit="deg")
T_AB = SE3(1, 2, 0) * SE3.Rz(90, unit="deg")
T_BC = SE3(1, 0, 0)
T_AC = T_AB * T_BC
T_CA = T_AC.inv()

print("旋转数组：\n", R.A)
print("位姿数组：\n", T_AB.A)
print("旋转部分：\n", T_AB.R)
print("平移部分：", T_AB.t)

p_C = np.array([1., 0., 0.])
p_A = T_AC.R @ p_C + T_AC.t
print("p_A：", p_A)  # [1, 4, 0]

assert np.allclose(p_A, [1, 4, 0])
assert np.allclose((T_CA * T_AC).A, np.eye(4), atol=1e-10)
assert np.allclose(T_AC.A, T_AB.A @ T_BC.A)

# 位置相同但乘法顺序不同，结果不同。
T_other = SE3.Rz(90, unit="deg") * SE3(1, 2, 0)
print("另一种顺序的平移：", T_other.t)  # 约 [-2, 1, 0]
```

| 数据类型 | 复合/矩阵乘法 | 求逆 | 取数组 |
|---|---|---|---|
| NumPy 数组 | `A @ B` | `np.linalg.inv(A)` | 已经是数组 |
| SO3/SE3 对象 | `A * B` | `A.inv()` | `A.A` |

不要把 NumPy 数组与对象的乘法规则混在一起。这里用 `.R @ p + .t` 显式完成点变换，也能让数组维度保持清晰。对象接口参见 [SO3](https://spatialmath-python.rai-inst.com/3d_orient_SO3.html) 与 [SE3](https://spatialmath-python.rai-inst.com/3d_pose_SE3.html)。

## 15. 批量处理点与可视化

### 15.1 一次变换多个点

约定 `P_B` 每一列是一个点，形状为 `(3, N)`：

```python
import numpy as np
from spatialmath import SE3

T_AB = (SE3(1, 2, 0) * SE3.Rz(90, unit="deg")).A
R_AB = T_AB[:3, :3]
t_AB = T_AB[:3, 3]

P_B = np.array([
    [0., 1., 0.],
    [0., 0., 1.],
    [0., 0., 0.]
])

# t_AB[:, None] 把 (3,) 变成 (3,1)，让平移加到每一列。
P_A = R_AB @ P_B + t_AB[:, None]
print(P_A)  # 各列约为 [1,2,0]、[1,3,0]、[0,2,0]

for i in range(P_B.shape[1]):
    expected = R_AB @ P_B[:, i] + t_AB
    assert np.allclose(P_A[:, i], expected)

# 如果原数据是每行一个点，形状为 (N,3)，应使用以下形式。
P_B_rows = P_B.T
P_A_rows = P_B_rows @ R_AB.T + t_AB
assert np.allclose(P_A_rows, P_A.T)
```

注意：恰好有 3 个点时，点云矩阵是 3×3，单看形状无法区分每行一个点还是每列一个点。必须说明数据约定。

### 15.2 画出两个坐标系

下面使用 Matplotlib 绘制坐标轴，运行后在支持图形界面的环境弹出窗口，不自动保存图片。红、绿、蓝分别代表 x、y、z 轴。

```python
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE3


def draw_frame(ax, T, name, length=0.5):
    origin = T[:3, 3]
    for i, color in enumerate(["r", "g", "b"]):
        direction = T[:3, i] * length
        ax.quiver(*origin, *direction, color=color)
    ax.text(*origin, name)


T_AB = (SE3(1, 2, 0) * SE3.Rz(90, unit="deg")).A
p_B = np.array([1., 0., 0.])
p_A = T_AB[:3, :3] @ p_B + T_AB[:3, 3]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
draw_frame(ax, np.eye(4), "A")
draw_frame(ax, T_AB, "B")
ax.scatter(*p_A, color="black")
ax.text(*p_A, "P")
ax.set(xlabel="x (m)", ylabel="y (m)", zlabel="z (m)",
       xlim=(-1, 4), ylim=(-1, 4), zlim=(-1, 4))
ax.set_box_aspect([1, 1, 1])
plt.show()
```

`*origin` 在函数调用中表示把三个坐标展开成三个参数。它不是这里的矩阵乘法。观察图像时，检查 B 的 x 轴是否指向 A 的正 y 方向。

## 16. 综合案例：相机坐标转换到机器人基座

设：

- W：世界坐标系。
- B：机器人基座坐标系。
- C：相机坐标系。
- 已知 `T_WB`、`T_WC`，相机测得点坐标 `p_C`。
- 目标：求 `p_B`。

先写坐标系关系，不急着写代码：

$$T_{WB}T_{BC}=T_{WC},\quad T_{BC}=T_{WB}^{-1}T_{WC},\quad p_B=T_{BC}p_C.$$

最后一个式子使用齐次坐标；如果使用三维坐标，需要拆成旋转加平移。

```python
import numpy as np
from spatialmath import SE3

np.set_printoptions(precision=4, suppress=True)

T_WB = SE3(1, 0, 0)
T_WC = SE3(1, 2, 0) * SE3.Rz(90, unit="deg")
p_C = np.array([1., 0., 0.])

T_BC = T_WB.inv() * T_WC
p_B = T_BC.R @ p_C + T_BC.t
print("点在基座中的坐标：", p_B)  # 约 [0, 3, 0]
assert np.allclose(p_B, [0, 3, 0], atol=1e-10)

# 验证：两条路径得到同一个世界坐标。
p_W_via_camera = T_WC.R @ p_C + T_WC.t
p_W_via_base = T_WB.R @ p_B + T_WB.t
assert np.allclose(p_W_via_camera, p_W_via_base)

# 再反向转换一次，找回相机测量值。
T_CB = T_BC.inv()
p_C_back = T_CB.R @ p_B + T_CB.t
assert np.allclose(p_C_back, p_C)
print("闭环验证通过")
```

这只是坐标换算示例。实际视觉系统中的像素坐标不能直接当作三维米制坐标输入；需要相机内参和深度等信息，属于后续内容。

## 17. 常见错误与速查

| 现象 | 首先检查 | 修正方向 |
|---|---|---|
| `rpy2r` unknown import symbol | 是否从 `roboticstoolbox` 导入 | 改为 `spatialmath.base` |
| `Panda` 未导出提示 | 库的导出声明与实际路径 | 使用 `from roboticstoolbox.models.URDF import Panda` |
| `ModuleNotFoundError` | 编辑器与终端解释器是否一致 | 检查 `sys.executable` |
| 矩阵结果尺寸奇怪 | `*`、`@`、数组 `shape` | 区分逐元素运算和矩阵乘法 |
| 向量相加后变成 3×3 | 是否混用 `(3,)` 和 `(3,1)` | 统一维度 |
| 90° 结果不对 | 是否把 90 当成弧度 | `np.deg2rad` 或 `unit="deg"` |
| 几何方向不对 | `R_AB` 含义、旋转顺序、参考轴 | 先写坐标系和映射方向 |
| 逆变换平移不对 | 是否只取 `-t` | 应为 `-R.T @ t` |
| 输出有 `6e-17` | 浮点近似 | 用容差检查，不必强行置零 |
| 角度恢复后不一样 | 是否为另一组等价角或奇异点 | 比较旋转矩阵 |
| 修改副本影响原数组 | 是否只是 `B = A` | 使用 `.copy()` |

建议每个程序至少检查三件事：输入单位、矩阵维度、坐标系方向。然后用一种独立方法验证，例如正逆变换、分步与连乘、手写与库函数互相核对。

常用语法速查：

| 目的 | 写法 |
|---|---|
| 三维坐标 | `np.array([x, y, z], dtype=float)` |
| 单位阵 | `np.eye(3)` 或 `np.eye(4)` |
| 零数组 | `np.zeros((3, 3))` |
| 取旋转 | `T[:3, :3]` |
| 取平移 | `T[:3, 3]` |
| 数组矩阵乘法 | `A @ B` |
| 长度 | `np.linalg.norm(v)` |
| 角度转弧度 | `np.deg2rad(angle)` |
| 弧度转角度 | `np.rad2deg(angle)` |
| 检查近似相同 | `np.allclose(A, B)` |
| RPY 创建旋转 | `SO3.RPY([r,p,y], unit="deg", order="zyx")` |
| 创建平移 | `SE3(x, y, z)` |
| SE3 对象求逆 | `T.inv()` |
| 对象转 NumPy | `T.A` |

## 18. 独立练习、参考答案与学习顺序

### 18.1 先独立完成

1. 用 NumPy 手写绕 z 轴旋转 180° 的矩阵，计算它对 `[1, 2, 3]` 的作用。
2. B 相对 A 绕 z 轴旋转 90°，B 原点在 A 中为 `[2, 0, 1]`。点在 B 中为 `[0, 1, 0]`，求它在 A 中的位置。
3. 对第 2 题构造齐次变换，手写逆变换，找回输入点。
4. `T_AB` 是沿 A 的 x 方向平移 1 米；`T_BC` 是相对 B 绕 z 轴旋转 90°且原点重合。求 C 中点 `[1, 0, 0]` 在 A 中的位置。
5. 令 `T_AB` 与第 2 题相同，求 B 中自由矢量 `[0, 1, 0]` 在 A 中的表示。
6. 用 `[10, 20, 30]` 度的 ZYX-RPY 创建旋转矩阵，再恢复角度并重新创建矩阵，检查两次的矩阵一致。
7. 绕 `[1, 1, 1]` 方向旋转 120°，计算它对 `[1, 0, 0]` 的作用。先将旋转轴单位化。
8. 将综合案例的 `T_WB` 改为 `SE3(2, 0, 0)`，其他不变，重新求 `p_B`，并验证世界坐标一致。

### 18.2 参考答案

先记录自己的预测，再展开答案。它们是自行构造的入门练习，不是课本习题答案的抄录。

<details>
<summary>展开完整参考程序</summary>

```python
import numpy as np
from spatialmath import SE3, SO3
from spatialmath.base import rpy2r, tr2rpy

# 1：约 [-1, -2, 3]
theta = np.deg2rad(180)
c, s = np.cos(theta), np.sin(theta)
R = np.array([[c, -s, 0.], [s, c, 0.], [0., 0., 1.]])
assert np.allclose(R @ [1, 2, 3], [-1, -2, 3])

# 2：约 [1, 0, 1]
R_AB = SO3.Rz(90, unit="deg").A
t_AB = np.array([2., 0., 1.])
p_B = np.array([0., 1., 0.])
p_A = R_AB @ p_B + t_AB
assert np.allclose(p_A, [1, 0, 1], atol=1e-10)

# 3：分块构造原变换与逆变换
T_AB = np.eye(4)
T_AB[:3, :3] = R_AB
T_AB[:3, 3] = t_AB
T_BA = np.eye(4)
T_BA[:3, :3] = R_AB.T
T_BA[:3, 3] = -R_AB.T @ t_AB
assert np.allclose(T_BA @ np.append(p_A, 1), np.append(p_B, 1))

# 4：约 [1, 1, 0]
T_AC = SE3(1, 0, 0) * SE3.Rz(90, unit="deg")
assert np.allclose(T_AC.R @ [1, 0, 0] + T_AC.t, [1, 1, 0])

# 5：约 [-1, 0, 0]，不加平移
assert np.allclose(R_AB @ [0, 1, 0], [-1, 0, 0], atol=1e-10)

# 6：比较旋转矩阵
R = rpy2r([10, 20, 30], unit="deg", order="zyx")
angles = tr2rpy(R, unit="deg", order="zyx")
assert np.allclose(rpy2r(angles, unit="deg", order="zyx"), R)

# 7：约 [0, 1, 0]
axis = np.array([1., 1., 1.])
axis /= np.linalg.norm(axis)
R = SO3.AngVec(120, axis, unit="deg").A
assert np.allclose(R @ [1, 0, 0], [0, 1, 0], atol=1e-10)

# 8：约 [-1, 3, 0]
T_WB = SE3(2, 0, 0)
T_WC = SE3(1, 2, 0) * SE3.Rz(90, unit="deg")
p_C = np.array([1., 0., 0.])
T_BC = T_WB.inv() * T_WC
p_B = T_BC.R @ p_C + T_BC.t
assert np.allclose(p_B, [-1, 3, 0])
assert np.allclose(T_WB.R @ p_B + T_WB.t, T_WC.R @ p_C + T_WC.t)

print("8 道练习全部检查通过")
```

</details>

### 18.3 建议学习顺序

| 阶段 | 学习范围 | 过关标准 |
|---|---|---|
| 第一次 | 1–5 节 | 会导入、写数组、检查 shape、使用函数与 @ |
| 第二次 | 6–7 节 | 不看答案写出三个基本旋转矩阵，解释旋转顺序 |
| 第三次 | 8–11 节 | 会构造 T、求逆、连乘，分清点和自由矢量 |
| 第四次 | 12–14 节 | 明确角度顺序与单位，会用对象和数组两种写法 |
| 第五次 | 15–16 节 | 独立完成相机到基座的坐标换算与闭环验证 |
| 复习 | 18 节 | 先手算预测，独立实现，再和答案比较 |

遇到问题时，把具体代码、输出、你预期的结果一起发来。尤其可以追问“这一行对应哪个数学公式”或“这个矩阵把谁的坐标变成谁的坐标”。下一阶段学操作臂正运动学时，会反复使用这里的变换连乘。

## 资料与范围说明

- 工作空间课本：[《机器人学导论》原书第 4 版](../机器人学导论(原书第4版)(Wx-Library).pdf)，第二章“空间描述和变换”，PDF 第 24–54 页。章节对应涵盖描述、映射、算子、变换计算、变换方程、其他姿态描述与自由矢量；本文采用独立编写的教学例子。
- [NumPy 官方入门](https://numpy.org/doc/stable/user/absolute_beginners)：数组基础。
- [NumPy allclose](https://numpy.org/doc/stable/reference/generated/numpy.allclose)：数值近似比较。
- [SpatialMath 三维函数](https://spatialmath-python.rai-inst.com/func_3d.html)：转换函数、角度单位与约定。
- [SpatialMath SO3](https://spatialmath-python.rai-inst.com/3d_orient_SO3.html)、[SE3](https://spatialmath-python.rai-inst.com/3d_pose_SE3.html)：对象接口。
- [SpatialMath 单位四元数](https://spatialmath-python.rai-inst.com/3d_orient_unitquaternion.html)：四元数约定与转换。

本文重点是将第二章数学写成程序。不会覆盖完整 Python 标准库，也没有加入后续 DH 参数、雅可比、动力学或控制内容。四元数与绘图可在首次阅读时跳过，待旋转矩阵与齐次变换熟练后补学。

验证记录（2026-11-11）：已从本文提取全部 22 个 Python 代码块，在工作空间 `daily/.venv` 中分别使用独立变量空间执行，全部通过，包含参考答案中的数值断言。绘图代码以 Agg 无窗口后端执行通过；未检查桌面弹窗的显示效果。
