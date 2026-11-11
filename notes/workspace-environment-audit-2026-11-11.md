# 工作空间环境审计与推荐方案

日期：2026-11-11。范围：robot-learning-log 的根配置、daily、exercises、独立 Python/C++ 项目、ROS 练习区、CI、当前本机运行环境。此次未修改配置、依赖或用户已有改动，仅新增本报告。不是整台机器或全部课程源码的安全审计。

## 结论

现有分环境架构合理，主要基础功能可用，不需要推倒重建。建议采用“一个学习仓库、多套独立环境、明确运行入口”的方案。当前存在一个明确的依赖选型错误，以及编辑器资源浪费、ROS 环境复现不完整等问题。

## 已确认的问题

| 优先级 | 位置 | 证据与影响 | 建议 |
|---|---|---|---|
| 高 | daily/pyproject.toml 中 pinocchio>=0.5.1 | 已安装包元数据为 nose 测试框架插件；import pinocchio 虽成功但没有 Model，不能用于机器人动力学 | 若目标是机器人 Pinocchio，移除同名测试插件，使用官方发行包 pin；重新锁定后验证 Model、数据结构和最小动力学计算 |
| 中 | .vscode/c_cpp_properties.json | 全递归扫描 /usr/include/**、ROS include/**，limitSymbolsToIncludedHeaders=false；browse.vc.db 实测 1,963,114,496 字节，约 1.83 GiB | 根目录仅配置 minilinalg 的编译数据库与必要头文件；ROS 索引留在 ROS 工作区。缩小范围、关闭编辑器后再重建索引；当前未删除数据库 |
| 中 | ROS 外部虚拟环境 | scipy、cv2、torch、onnxruntime 实际来自 ~/.local/lib/python3.10/site-packages；并非该 venv 自身完整提供 | 将需要的非 apt 包显式声明并安装到 ROS venv，记录 apt 依赖与约束；补齐后才考虑 PYTHONNOUSERSITE=1 |
| 中 | ROS 隔离后的兼容性 | 临时设置 PYTHONNOUSERSITE=1 后 torch/onnxruntime 缺失，scipy 回退至系统 1.8.0，且警告 numpy 1.26.4 超出支持范围 | 不要直接全局禁用用户包；先补齐本地依赖并验证 numpy/scipy/cv_bridge，再开启隔离 |
| 中 | .envrc | 当前 direnv status 显示 allowed=false，当前进程也未加载；文件存在不代表终端隔离生效 | 可信交互式终端执行 direnv allow；脚本继续显式清理变量，不能依赖交互式 hook。当前检查进程未发现 PYTHONPATH 泄漏 |
| 中 | exercises/uv.lock | 无配套 pyproject.toml，锁中项目名称为 daily，内容与 daily 当前锁也不同 | exercises 既然共享 daily 环境，就只保留唯一依赖来源，确认无用途后移除孤立锁；运行时显式 --project daily |
| 中 | robotics_courses 两个目录 | ModernRobotics 与 ModernRoboticsCpp 各含嵌套 .git，父仓库显示整个目录未跟踪，没有注册子模块 | 选择显式 submodule 或外部克隆并记录 URL/commit；普通 git add 不会自动可靠纳入内部文件。不要直接删除内层 .git |
| 低 | 编辑器可迁移性 | 根 cmake.sourceDirectory 与 ROS 解释器含 /home/ryder 绝对路径；本地 C++ fallback 为 C++17，项目构建为 C++20；c_cpp_properties.json 被忽略 | 改成 workspaceFolder/env:HOME 相对引用，fallback 统一 C++20，以编译数据库为准；把需共享的配置纳入版本控制 |
| 低 | CI | 只覆盖 r1 Python 与 C++；uv sync 未使用 --locked；uv 版本不固定；CI C++ 在 build/，本地在 build/r3，且 CI 为 Release、本地为 sanitizer Debug | CI 固定 uv 工具版本、uv sync --locked，统一路径；增加 daily 核心导入检查。教学骨架的预期失败测试不要当成整仓库失败 |
| 低 | Python 版本策略 | daily 仅声明 >=3.13，未固定解释器 minor；r1 有 .python-version | daily 增加 3.13 的解释器 pin。requires-python 表示兼容范围，.python-version 表示开发选择；有证据后再扩大支持范围 |

## 正常项与验证

- 系统 Ubuntu 22.04.5，系统 Python 3.10.12；daily 与 r1 使用独立 Python 3.13.15，ROS 使用系统派生 3.10 venv。两套 Python 并存本身不是异常。
- daily 的 numpy、matplotlib、scipy、modern_robotics、roboticstoolbox、mujoco、screws 均可导入。仅导入不代表图形渲染、GPU、仿真或所有算法均已验证。
- r1 pytest：2/2 通过。
- 现有 C++ 构建 ctest：沙箱内 LeakSanitizer 因运行限制报错，沙箱外 4/4 通过。未重新从零下载和构建 GoogleTest。
- daily 与 r1 的 uv lock --check --offline 均通过；这只证明清单与锁一致，不保证选中的包符合业务目标。
- ROS 包 rclpy、tf2_ros、cv_bridge、moveit、pymoveit2 等可导入。未运行 DDS 通信、MoveIt 规划或 GPU 推理。
- scripts 的 bash 语法检查通过。
- 磁盘可用约 73 GB，内存约 31 GiB，当前无磁盘/内存紧张证据。
- Matplotlib 报告配置目录不可写是本次沙箱写权限边界导致，不能据此认定宿主目录权限损坏。
- Git main 比本地 origin/main 引用领先 1 个提交；未联网 fetch，无法据此判断远端最新状态。已有 daily 清单/锁改动、文件删除和未跟踪文件，均保留。这些工作中状态不等于仓库损坏。
- ROS scripts/ros 支持叠加 install/setup.bash；F5 配置只注入基础 ROS 环境，README 已说明 overlay 限制，后续自建功能包调试需统一入口。

## 适合本仓库的推荐架构

| 区域 | 环境 | 依赖与入口 |
|---|---|---|
| daily + exercises | daily/.venv，Python 3.13 | daily/pyproject.toml + uv.lock；基础数值包常驻，较重仿真库按实际需要分组或迁至独立项目；从根目录显式 --project daily |
| projects/r1-robomath 等 | 各项目独立 .venv | 各自 pyproject、lock、Python pin；不与 ROS 合并 |
| C++ minilinalg | 系统编译器、CMake、GoogleTest | 统一 build/r3；可补 CMakePresets.json，分别定义 Debug sanitizer 和 Release；IDE 读取 compile_commands.json |
| ros2robotics_logs | Humble + 系统 Python 3.10 派生 venv | 保留 --system-site-packages 以使用 apt ROS 包；另列 apt 清单及 Python 约束；显式 source 后构建/运行 |
| 课程参考源码 | 显式版本引用 | submodule 或仓库外克隆；不纳入无关索引 |

不建议把所有目录并成一个 uv workspace：官方 workspace 共享锁与环境，当前 ROS 与普通 Python 的解释器和依赖边界不同，强行统一会增加约束。也没有现有故障证据要求全仓库 Docker 化；日常数值练习保持 uv，ROS 保持本机工具链，更符合当前学习成本。容器可作为未来部署/异机复现的补充。

建议普通 Python 入口统一使用已有 scripts/py.sh，并加 --locked，例如：

```bash
./scripts/py.sh run --locked --project daily python daily/2026-11-10/ITR01.py
./scripts/py.sh run --locked --project projects/r1-robomath pytest -q
```

ROS 继续使用独立入口：

```bash
cd ros2robotics_logs
./scripts/ros scripts/hello_ros.py
```

后续补环境检查脚本时应分别检查：包版本、实际导入路径、Pinocchio Model、numpy/scipy 兼容性、基础测试与编译数据库存在性。不要用“import 没报错”替代功能验证。

## 实施顺序

1. 修正 Pinocchio 依赖并验证功能。
2. 缩小 C++ 索引范围，统一 C++20 和可迁移路径，再重建索引。
3. 记录并补齐 ROS 本地依赖，处理 numpy/scipy 组合，随后验证用户包隔离。
4. 明确课程仓库管理方式、清理孤立锁文件、固定 daily 解释器。
5. 完善 CI 锁验证与最小导入检查，统一构建和调试入口。

## 官方依据

- Pinocchio 官方安装说明：PyPI 发行包名是 pin，Python 导入名仍为 pinocchio：https://stack-of-tasks.github.io/pinocchio/download.html
- uv 锁定与同步：--locked 在锁需更新时失败，普通 uv run/sync 可自动更新锁：https://docs.astral.sh/uv/concepts/projects/sync/
- uv 工作区共享依赖解析和环境的约束：https://docs.astral.sh/uv/concepts/projects/workspaces/
- uv Python 版本选择机制：https://docs.astral.sh/uv/concepts/python-versions/

ROS 官方 Python packages 页本次被访问保护拦截，未将无法读取的页面作为事实依据。ROS 相关结论基于当前本机配置与实际导入路径。


## 执行结果（2026-11-11）

- 已替换为 pin 4.1.0，移除同名 nose 插件；6 自由度机械臂质量矩阵计算通过，主要科学计算/机器人库检查通过。
- C++ 索引范围已缩小，标准统一为 C++20，配置使用相对路径；无占用的旧索引已清理，.vscode 从约 1.9 GB 降至 16 KB。
- ROS 45 个锁定版本全部匹配，运行器禁用用户 site-packages，优先使用 robot-tools；独立环境导入、数值计算、图像转换与 PyTorch 基础计算通过，问候节点启动并退出正常。
- ROS 大型包采用硬链接复用，约 5.79 GiB 与既有安装共享数据；元数据和入口脚本单独保存。不要直接原地编辑共享的第三方包文件，更新依赖使用包管理器。
- daily 解释器固定为 3.13，锁文件同步完成；环境逻辑大小由约 597 MiB 增至 980 MiB，新增的是实际使用的 Pinocchio 及其原生库。
- exercises 使用 daily 的唯一依赖清单，孤立锁已移除；课程源码保留独立克隆，来源和固定提交记录于 robotics_courses/README.md。
- README 已精简为用途、目录和使用命令；新增 ROS 依赖清单与 Attach 调试入口，CI 固定 uv 并使用 --locked，新增 daily 检查。
- 已授权 direnv；注入外部 Python 变量的隔离检查通过。
- 统一 scripts/check.sh 检查通过：Python 2/2、C++ 4/4（Debug + ASan/UBSan）；两个正式项目锁文件检查、脚本/配置语法及 git diff --check 通过。
- 检查过程中发现 --project 不切换工作目录，已将 r1 测试入口改为 --directory，避免误收集未完成的练习题。

仅完成本机验证，未触发 GitHub 托管 CI，也未验证 GPU 推理、MoveIt 规划及图形仿真。未提交或推送 Git；用户既有的学习代码改动保留。空间数字区分逻辑大小与硬链接共享数据，不将整个 ROS 环境大小算作新增占用。
