# daily 使用说明

`daily/` 是一个独立的 uv 项目，所有每日练习共享 `daily/.venv`。这样编辑器能选解释器、自动补全，不会标红。

## 常用命令

```bash
cd ~/robot-learning-log/daily

# 加包（只改 daily 的环境，不影响 projects）
uv add scipy
uv add --dev pytest ruff

# 跑当天脚本
uv run python 2026-11-01/python/ex01.py

# 跑 daily 里的测试
uv run pytest 2026-11-01/python -q
```

## 一次性包（不想改 daily 依赖时）

```bash
cd ~/robot-learning-log
env -u PYTHONPATH uv run --with seaborn python daily/2026-11-01/python/plot.py
```

`--with` 用临时环境，不修改 `daily/pyproject.toml`；适合试一个包，不适合长期开发。

## 为什么不给每个日期建 .venv

- 一天一个 `.venv` 会有几十个环境，安装慢、占空间、难管理；
- VS Code 一次只能选一个解释器，几十个环境反而更乱；
- `daily` 一个共享环境 + `uv.lock` 足够；需要冲突版本时再用 `--with` 或单独项目。

## 什么时候升级成项目

如果某个练习连续做 3 天以上，或需要固定依赖版本/多个源文件/测试，就把它移到 `projects/`：

```bash
cd projects
uv init --package my_experiment
cd my_experiment
uv add numpy
uv add --dev pytest
```

然后按项目方式管理。